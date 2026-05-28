import os
import sys
import unittest
from unittest import mock

import litellm

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.llm_config import apply_litellm_input_hook, gemini_llm, groq_llm, strip_cache_breakpoint_params
from crew_orchestrator import TripCrewOrchestrator, clean_json_output


class TestTripCrewOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = TripCrewOrchestrator()

    def test_extract_json_payload_from_markdown(self):
        raw_output = "```json\n{\"destination\": \"Goa\", \"days\": 7}\n```"
        parsed = self.orchestrator._extract_json_payload(raw_output)

        self.assertEqual(parsed["destination"], "Goa")
        self.assertEqual(parsed["days"], 7)

    def test_clean_json_output_strips_markdown_fences(self):
        cleaned = clean_json_output("```json\n{\"status\": \"ok\"}\n```")

        self.assertEqual(cleaned, '{"status": "ok"}')

    def test_extract_json_payload_from_plain_text(self):
        raw_output = "Result: {\"status\": \"ok\"}"
        parsed = self.orchestrator._extract_json_payload(raw_output)

        self.assertEqual(parsed["status"], "ok")

    def test_strip_cache_breakpoint_params_removes_nested_key(self):
        payload = {
            "optional_params": {
                "cache_breakpoint": "marker",
                "temperature": 0.3,
            },
            "messages": [
                {
                    "role": "system",
                    "content": "test",
                    "cache_breakpoint": "marker",
                }
            ],
        }

        cleaned = strip_cache_breakpoint_params(payload)

        self.assertNotIn("cache_breakpoint", cleaned["optional_params"])
        self.assertNotIn("cache_breakpoint", cleaned["messages"][0])
        self.assertEqual(cleaned["optional_params"]["temperature"], 0.3)

    def test_apply_litellm_input_hook_sanitizes_groq_requests(self):
        captured = {}

        def fake_completion(*args, **kwargs):
            captured["model"] = kwargs.get("model")
            captured["messages"] = kwargs.get("messages")
            captured["optional_params"] = kwargs.get("optional_params")
            return "ok"

        original_completion = litellm.completion
        litellm.completion = fake_completion

        try:
            apply_litellm_input_hook(force=True)
            litellm.completion(
                model="groq/llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "hello"}],
                optional_params={"cache_breakpoint": "marker", "temperature": 0.3},
            )

            self.assertEqual(captured["model"], "groq/llama-3.3-70b-versatile")
            self.assertEqual(captured["messages"][0]["content"], "hello")
            self.assertEqual(captured["optional_params"]["temperature"], 0.3)
            self.assertNotIn("cache_breakpoint", captured["optional_params"])
        finally:
            litellm.completion = original_completion

    def test_apply_litellm_input_hook_preserves_non_groq_calls(self):
        captured = {}

        def fake_completion(*args, **kwargs):
            captured["model"] = kwargs.get("model")
            captured["messages"] = kwargs.get("messages")
            return "ok"

        original_completion = litellm.completion
        litellm.completion = fake_completion

        try:
            apply_litellm_input_hook(force=True)
            litellm.completion(
                model="gemini/gemini-2.0-flash",
                messages=[{"role": "system", "content": "hello"}],
            )

            self.assertEqual(captured["model"], "gemini/gemini-2.0-flash")
            self.assertEqual(captured["messages"][0]["content"], "hello")
        finally:
            litellm.completion = original_completion

    def test_should_retry_with_fallback_detects_rate_limit_error(self):
        should_retry = self.orchestrator._should_retry_with_fallback(
            "RateLimitError: GroqException - Rate limit reached for model"
        )

        self.assertTrue(should_retry)

    def test_apply_fallback_llms_switches_all_agents(self):
        self.orchestrator.primary_llm = groq_llm
        self.orchestrator.fallback_llm = gemini_llm

        self.orchestrator._reset_default_llms()
        self.orchestrator._apply_fallback_llms()

        for agent in self.orchestrator.all_agents.values():
            self.assertIs(agent.llm, gemini_llm)

    def test_execute_crew_with_retry_retries_then_returns_success(self):
        class DummyCrew:
            def __init__(self):
                self.calls = 0

            def kickoff(self):
                self.calls += 1
                if self.calls == 1:
                    raise RuntimeError("Rate limit reached. Please try again in 13.82s.")
                return "{\"status\": \"ok\"}"

        dummy_crew = DummyCrew()

        with unittest.mock.patch("crew_orchestrator.time.sleep") as mock_sleep:
            result = self.orchestrator._execute_crew_with_retry(dummy_crew, max_attempts=2)

        self.assertEqual(result, "{\"status\": \"ok\"}")
        self.assertEqual(dummy_crew.calls, 2)
        mock_sleep.assert_called_once()
        self.assertEqual(mock_sleep.call_args[0][0], 13.82)

    def test_execute_crew_with_retry_parses_gemini_retry_delay(self):
        class DummyCrew:
            def __init__(self):
                self.calls = 0

            def kickoff(self):
                self.calls += 1
                if self.calls == 1:
                    raise RuntimeError("Quota exceeded. Please retry in 54.81901872s.")
                return "{\"status\": \"ok\"}"

        dummy_crew = DummyCrew()

        with unittest.mock.patch("crew_orchestrator.time.sleep") as mock_sleep:
            result = self.orchestrator._execute_crew_with_retry(dummy_crew, max_attempts=2)

        self.assertEqual(result, "{\"status\": \"ok\"}")
        self.assertEqual(dummy_crew.calls, 2)
        mock_sleep.assert_called_once()
        self.assertEqual(mock_sleep.call_args[0][0], 54.81901872)

    def test_parse_result_returns_structured_error_for_invalid_output(self):
        parsed = self.orchestrator._parse_result("this is not valid json")

        self.assertEqual(parsed["error"], "Crew AI failed to return valid JSON")
        self.assertIn("this is not valid json", parsed["raw_output"])

    def test_execute_crew_with_retry_propagates_timeout(self):
        class DummyCrew:
            pass

        with mock.patch.object(self.orchestrator, "_run_crew_with_timeout", side_effect=TimeoutError("timed out")):
            with self.assertRaises(TimeoutError):
                self.orchestrator._execute_crew_with_retry(DummyCrew(), max_attempts=1, execution_timeout=0.01)

    def test_plan_trip_returns_offline_fallback_when_all_providers_fail(self):
        sample_inputs = {
            "destination": "Goa, India",
            "startDate": "2026-06-15",
            "endDate": "2026-06-21",
            "kids": 1,
            "adults": 2,
            "seniors": 1,
            "budgetMode": "Premium",
            "foodPref": "Veg",
            "travelStyle": "Relaxed",
            "interests": ["Nature", "Food", "History"],
        }

        with mock.patch.object(self.orchestrator, "_execute_crew_with_retry", side_effect=[
            RuntimeError("Rate limit reached for model"),
            RuntimeError("429 RESOURCE_EXHAUSTED. quota exceeded"),
        ]), mock.patch.object(self.orchestrator, "_build_trip_crew", return_value=object()), \
             mock.patch.object(self.orchestrator, "_apply_fallback_llms"), \
             mock.patch.object(self.orchestrator, "_reset_default_llms"):
            result = self.orchestrator.plan_trip(sample_inputs)

        self.assertEqual(result["status"], "offline_fallback")
        self.assertIn("429 RESOURCE_EXHAUSTED", result["provider_error"])
        self.assertEqual(result["itinerary"]["destination"], "Goa, India")
        self.assertEqual(result["itinerary"]["duration_days"], 6)
        self.assertEqual(result["recommendations"]["food"][0]["preference"], "Veg")


if __name__ == "__main__":
    unittest.main()
