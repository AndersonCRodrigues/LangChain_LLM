import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from gemini import googleai_client

set_llm_cache(InMemoryCache())

llm = googleai_client
mensagens = [
    SystemMessage(content="Você é um assistente irônico."),
    HumanMessage(content="Qual o quinto dia da semana?"),
]

inicio = time.time()
chat = llm.invoke(mensagens)
fim = time.time()

print(chat.content)
print(f"Tempo de execução sem cache: {fim - inicio:.6f} segundos")

inicio = time.time()
chat = llm.invoke(mensagens)
fim = time.time()

print(chat.content)
print(f"Tempo de execução com cache: {fim - inicio:.6f} segundos")
