import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.providers.ai_provider import AIProvider


load_dotenv()


class GeminiProvider(AIProvider):

    def __init__(
        self,
        model: str = "gemini-3.5-flash-lite"
    ):
        self.model = model

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise Exception(
                "GEMINI_API_KEY not found"
            )

        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=api_key
        )

    def generate_response(
        self,
        messages: list
    ) -> str:

        response = self.llm.invoke(messages)

        content = response.content

        # Gemini may return structured content
        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, dict):

                    if item.get("type") == "text":
                        text_parts.append(
                            item.get("text", "")
                        )

                elif isinstance(item, str):
                    text_parts.append(item)

            return "".join(text_parts)

        return str(content)