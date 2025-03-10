from gemini import googleai_client
from langchain.prompts import PromptTemplate

llm = googleai_client

prompt = PromptTemplate.from_template(
    """
    Escolha o melhor nome para mim sobre uma
    empresa que desenvolve soluções em {produto}
    """
)

chain = prompt | llm
produto = "LLMs com LangChain"
resposta = chain.invoke(produto)
print(resposta.content)
