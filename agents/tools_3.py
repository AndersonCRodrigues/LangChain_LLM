from langchain.agents import tool
from pydantic import BaseModel, Field


class InformacoesFilmeArgs(BaseModel):
    titulo_filme: str = Field(
        description="Título do filme",
        examples=["Inception", "The Matrix"],
    )


@tool(args_schema=InformacoesFilmeArgs)
def obter_informacoes_filme(titulo_filme: str):
    """Retorna informações sobre um filme"""
    return (
        f'O filme "{titulo_filme}" foi lançado em 2010, '
        "dirigido por Christopher Nolan."
    )


print(obter_informacoes_filme.invoke({"titulo_filme": "Inception"}))
