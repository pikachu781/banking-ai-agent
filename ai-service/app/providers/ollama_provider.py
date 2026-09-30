from langchain_ollama import ChatOllama

from app.providers.ai_provider import AIProvider


class OllamaProvider(AIProvider):

    def __init__(self, model: str = "mistral:latest"):
        self.model = model

        self.llm = ChatOllama(
            model=self.model,
            temperature=0
        )

    def generate_response(
        self,
        messages: list
    ) -> str:

        response = self.llm.invoke(messages)

        return response.content