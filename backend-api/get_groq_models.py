import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

response = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)
if response.status_code == 200:
    for model in response.json()['data']:
        print(model['id'])
else:
    print(response.text)
