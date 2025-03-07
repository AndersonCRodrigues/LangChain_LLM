from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from gemini import googleai_client

llm = googleai_client

mensagens = [
    SystemMessage(content="Você é um assistente que responde com irônia"),
    HumanMessage(content="Qual é o primeiro dia da semana?"),
    AIMessage(content="Domingo"),
    HumanMessage(content="Qual o terceiro dia da semana?"),
    AIMessage(content="Terça-Feira"),
    HumanMessage(content="Qual o último dia da semana?"),
]

chat = googleai_client.invoke(mensagens)

print(chat.content)
