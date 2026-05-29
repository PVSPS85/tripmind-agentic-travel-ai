from litellm import completion
from dotenv import load_dotenv

load_dotenv()
models_to_test = [
    "gemini/gemini-2.0-flash-lite",
    "gemini/gemini-2.5-pro",
    "gemini/gemini-2.0-flash-001"
]

for model in models_to_test:
    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            temperature=0.4
        )
        print(f"{model} SUCCESS")
    except Exception as e:
        print(f"{model} FAILED: {str(e)}")

