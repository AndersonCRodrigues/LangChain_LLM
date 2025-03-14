import contextlib
import wikipedia
from langchain.agents import tool

wikipedia.set_lang("pt")


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


print(busca_wikipedia.invoke({"query": "langchain"}))
