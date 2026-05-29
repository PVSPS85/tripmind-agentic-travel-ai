import os
import litellm
from dotenv import load_dotenv

load_dotenv()

try:
    response = litellm.completion(
        model="gemini/gemini-pro",
        messages=[{"role": "user", "content": "Hello! Give me a 1 sentence summary of Tokyo."}]
    )
    print("SUCCESS!")
    print(response.choices[0].message.content)
except Exception as e:
    print("ERROR:", e)
