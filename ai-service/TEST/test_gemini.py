import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# Load .env
load_dotenv()


# Check API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY not found")


# Create Gemini LangChain model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    google_api_key=api_key
)


# Test
response = llm.invoke(
    "Say hello in one short sentence."
)


print("\n========== LANGCHAIN GEMINI TEST ==========")
print(response.content)