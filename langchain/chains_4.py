from gemini import googleai_client
from langchain.prompts import PromptTemplate

llm = googleai_client

prompt_nome = PromptTemplate(
    input_variables=["produto"],
    template="""
    Escolha apenas um nome para mim sobre uma
    empresa que desenvolve soluções em {produto}
    """,
)

prompt_descricao = PromptTemplate(
    input_variables=["nome_empresa"],
    template="""
    Sobre a empresa com nome {nome_empresa}.
    Informe uma descrição de até 20 palavras,
    incluindo o nome dela.
    """,
)

chain_nome = prompt_nome | llm

chain_descricao = prompt_descricao | llm

chain = chain_nome | chain_descricao

produto = "LLMs com LangChain"

resposta = chain.invoke({"produto": produto})
print(resposta)
