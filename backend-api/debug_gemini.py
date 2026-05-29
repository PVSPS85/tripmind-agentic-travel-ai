from litellm import completion
import os

try:
    response = completion(
        model="gemini/gemini-1.5-pro",
        messages=[{"role": "user", "content": "Hello"}],
        temperature=0.4
    )
    print("gemini-1.5-pro success:", response.choices[0].message.content)
except Exception as e:
    print(f"gemini-1.5-pro Error: {e}")

try:
    response = completion(
        model="gemini/gemini-pro",
        messages=[{"role": "user", "content": "Hello"}],
        temperature=0.4
    )
    print("gemini-pro success:", response.choices[0].message.content)
except Exception as e:
    print(f"gemini-pro Error: {e}")

