from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()
try:
    response = completion(
        model="groq/llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Hello! Please write a very long essay."}],
        temperature=0.4
    )
    print("SUCCESS: " + response.choices[0].message.content[:100])
except Exception as e:
    print(f"FAILED: {str(e)}")

