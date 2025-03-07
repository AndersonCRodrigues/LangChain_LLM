from langchain_core.messages import HumanMessage, SystemMessage
from gemini import googleai_client

llm = googleai_client

mensagens = [
    SystemMessage(content="Você é um assistente que responde com irônia"),
    HumanMessage(content="Qual o papel da memória cache?"),
]

chat = llm.invoke(mensagens)

print(chat.content)

print(chat.response_metadata)
