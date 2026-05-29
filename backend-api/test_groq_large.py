from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()
try:
    large_text = "word " * 12000
    response = completion(
        model="groq/llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"Summarize this: {large_text}"}],
        temperature=0.4
    )
    print("SUCCESS: " + response.choices[0].message.content[:100])
except Exception as e:
    print(f"FAILED: {str(e)}")

