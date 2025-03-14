from langchain.agents import tool
from pydantic import BaseModel, Field


class OperacaoMatematicaArgs(BaseModel):
    numero1: float = Field(description="Primeiro número", examples=[10, 5])
    numero2: float = Field(description="Segundo número", examples=[20, 3])
    operacao: str = Field(
        description="Operação a ser realizada", examples=["soma", "subtração"]
    )


@tool(args_schema=OperacaoMatematicaArgs)
def realizar_calculo(numero1: float, numero2: float, operacao: str):
    """Realiza operações matemáticas básicas"""
    if operacao == "soma":
        return numero1 + numero2
    elif operacao == "subtração":
        return numero1 - numero2
    else:
        return "Operação inválida"


resposta = realizar_calculo.invoke(
    {
        "numero1": 10,
        "numero2": 50,
        "operacao": "soma",
    }
)

print(resposta)
