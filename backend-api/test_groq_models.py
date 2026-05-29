import litellm
import os
from dotenv import load_dotenv

load_dotenv()

try:
    response = litellm.completion(
        model="groq/llama3-8b-8192",
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=10
    )
    print("SUCCESS llama3-8b-8192")
except Exception as e:
    print("ERROR llama3-8b-8192:", e)

try:
    response = litellm.completion(
        model="groq/llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "hi"}],
        max_tokens=10
    )
    print("SUCCESS llama-3.3-70b-versatile")
except Exception as e:
    print("ERROR llama-3.3-70b-versatile:", e)
