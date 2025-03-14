from langchain.prompts import ChatPromptTemplate
from langchain.agents import tool
import contextlib
import wikipedia
from gemini import googleai_client

llm = googleai_client


@tool
def busca_wikipedia(query: str):
    """Busca dados no wikipedia e retorna resumos de páginas para a query"""
    titulo_paginas = wikipedia.search(query)
    resumos = []
    for titulo in titulo_paginas[:3]:
        with contextlib.suppress(Exception):
            wiki_page = wikipedia.page(title=titulo, auto_suggest=True)
            resumos.append(f"Título: {titulo}\nResumo: {wiki_page.summary}")
    return "\n\n".join(resumos) if resumos else "Busca não teve retorno"


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente que sabe sobre futebol"),
        ("user", "{input}"),
    ]
)


chain = prompt | llm.bind_tools(
    [
        busca_wikipedia,
    ]
)

resposta = chain.invoke({"input": "olá"})
print(resposta.content)

resposta = chain.invoke(
    {
        "input": (
            "Quem foi melhor, Ronaldinho Gaúcho ou Messi? "
            "Justifique sem buscar informações externas."
        )
    }
)
print(resposta.content)
