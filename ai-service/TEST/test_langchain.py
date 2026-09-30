from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="mistral:latest",
    temperature=0
)


response = llm.invoke(
    "Say hello in one short sentence."
)


print("\n========== LANGCHAIN TEST ==========")
print(response.content)