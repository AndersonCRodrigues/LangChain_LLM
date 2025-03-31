from langchain.agents import tool
from pydantic import BaseModel, Field


class CalcularDistanciaArgs(BaseModel):
    cidade_origem: str = Field(
        description="CIdade de origem",
        examples=[
            "São Paulo",
            "Rio de Janeiro",
        ],
    )
    cidade_destino: str = Field(
        description="CIdade de destino",
        examples=[
            "Porto Alegre",
            "Curitiba",
        ],
    )


@tool(args_schema=CalcularDistanciaArgs)
def calcular_distancia(cidade_origem: str, cidade_destino: str):
    """Calcula a distância entre duas cidades"""
    return f"A distância entre {cidade_origem} e {cidade_destino} é de 300km"


resposta = calcular_distancia.invoke(
    {"cidade_origem": "São Paulo", "cidade_destino": "Porto Alegre"}
)
print(resposta)
