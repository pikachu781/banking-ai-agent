import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print("API KEY LOADED:", bool(api_key))

if not api_key:
    print("ERROR: OPENAI_API_KEY not found")
    exit()

print("KEY PREFIX:", api_key[:10])

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence."
            }
        ]
    )

    print("\nSUCCESS!")
    print("Model response:")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nOPENAI ERROR:")
    print(type(e).__name__)
    print(e)