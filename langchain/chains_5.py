from gemini import googleai_client
from langchain.chains import SequentialChain
from langchain.chains.llm import LLMChain
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
    input_variables=["nome_empresa", "produto"],
    template="""
    Sobre a empresa com o nome {nome_empresa} e que
    produz seguinte {produto}.
    Informe uma descrição de até 30 palavras de atividades dessa empresa
    """,
)

prompt_traducao = PromptTemplate(
    input_variables=["nome_empresa", "descricao_empresa"],
    template="""
    Escolha apenas um nome em espanhol para a empresa {nome_empresa},
    que possui a seguinte descrição: {descricao_empresa}.
    """,
)

chain_nome = LLMChain(
    llm=llm,
    prompt=prompt_nome,
    output_key="nome_empresa",
)
chain_descricao = LLMChain(
    llm=llm,
    prompt=prompt_descricao,
    output_key="descricao_empresa",
)
chain_traducao = LLMChain(
    llm=llm,
    prompt=prompt_traducao,
    output_key="nome_espanhol",
)

chain = SequentialChain(
    chains=[chain_nome, chain_descricao, chain_traducao],
    input_variables=["produto"],
    output_variables=[
        "nome_empresa",
        "descricao_empresa",
        "nome_espanhol",
    ],
    verbose=True,
)

produto = "LLMs com LangChain"

resposta = chain.invoke({"produto": produto})
print(resposta["produto"])
print(resposta["nome_empresa"])
print(resposta["descricao_empresa"])
print(resposta["nome_espanhol"])
