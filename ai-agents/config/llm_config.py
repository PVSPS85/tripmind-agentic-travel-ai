import functools
import os
import litellm
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

# Ensure keys are set for LiteLLM
if os.getenv("GOOGLE_API_KEY") and not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")


def strip_cache_breakpoint_params(payload):
    if isinstance(payload, dict):
        cleaned = {}
        for key, value in payload.items():
            if key == "cache_breakpoint":
                continue
            cleaned[key] = strip_cache_breakpoint_params(value)
        return cleaned
    if isinstance(payload, list):
        return [strip_cache_breakpoint_params(item) for item in payload]
    return payload


def sanitize_litellm_request_payload(model, messages=None, **kwargs):
    if not isinstance(model, str):
        return messages, kwargs

    provider = model.split("/", 1)[0].lower()
    if provider != "groq":
        return messages, kwargs

    sanitized_messages = strip_cache_breakpoint_params(messages)
    sanitized_kwargs = strip_cache_breakpoint_params(kwargs)
    return sanitized_messages, sanitized_kwargs


def apply_litellm_input_hook(force=False):
    if not force and getattr(litellm.completion, "_tripmind_cache_breakpoint_hook_applied", False):
        return

    original_completion = litellm.completion

    @functools.wraps(original_completion)
    def patched_completion(*args, **kwargs):
        model = kwargs.get("model") or (args[0] if args else None)
        messages = kwargs.get("messages")
        if len(args) > 1:
            messages = args[1]

        if isinstance(model, str) and model.lower().startswith("groq"):
            sanitized_kwargs = dict(kwargs)
            sanitized_kwargs.pop("messages", None)
            sanitized_kwargs.pop("model", None)
            sanitized_messages, sanitized_kwargs = sanitize_litellm_request_payload(model, messages=messages, **sanitized_kwargs)
            sanitized_kwargs["model"] = model
            sanitized_kwargs["messages"] = sanitized_messages
            return original_completion(**sanitized_kwargs)

        return original_completion(*args, **kwargs)

    patched_completion._tripmind_cache_breakpoint_hook_applied = True
    patched_completion._tripmind_cache_breakpoint_original = original_completion
    litellm.completion = patched_completion

    if hasattr(litellm, "acompletion"):
        original_acompletion = litellm.acompletion

        @functools.wraps(original_acompletion)
        async def patched_acompletion(*args, **kwargs):
            model = kwargs.get("model") or (args[0] if args else None)
            messages = kwargs.get("messages")
            if len(args) > 1:
                messages = args[1]

            if isinstance(model, str) and model.lower().startswith("groq"):
                sanitized_kwargs = dict(kwargs)
                sanitized_kwargs.pop("messages", None)
                sanitized_kwargs.pop("model", None)
                sanitized_messages, sanitized_kwargs = sanitize_litellm_request_payload(model, messages=messages, **sanitized_kwargs)
                sanitized_kwargs["model"] = model
                sanitized_kwargs["messages"] = sanitized_messages
                return await original_acompletion(**sanitized_kwargs)

            return await original_acompletion(*args, **kwargs)

        patched_acompletion._tripmind_cache_breakpoint_hook_applied = True
        patched_acompletion._tripmind_cache_breakpoint_original = original_acompletion
        litellm.acompletion = patched_acompletion


apply_litellm_input_hook()


class LLMConfig:
    # Use standard model identifiers
    @staticmethod
    def get_gemini_model():
        return LLM(
            model="gemini/gemini-2.0-flash", 
            temperature=0.4
        )

    @staticmethod
    def get_groq_model():
        # Llama 3.3 is the stable, high-performance default for Groq
        return LLM(
            model="groq/llama-3.3-70b-versatile",
            temperature=0.3
        )

gemini_llm = LLMConfig.get_gemini_model()
groq_llm = LLMConfig.get_groq_model()