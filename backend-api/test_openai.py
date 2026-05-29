from litellm import completion
from dotenv import load_dotenv

load_dotenv()
try:
    response = completion(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello"}],
        temperature=0.4
    )
    print("SUCCESS: " + response.choices[0].message.content)
except Exception as e:
    print(f"FAILED: {str(e)}")

