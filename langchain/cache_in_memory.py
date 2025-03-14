import time
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache
from gemini import googleai_client

cache = SQLiteCache(database_path="files/vector_store_cache.db")

set_llm_cache(cache)

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
