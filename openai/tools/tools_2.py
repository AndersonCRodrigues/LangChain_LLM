import json
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.Client()


def calcular_imc(peso, altura):
    if altura <= 0 or peso <= 0:
        return json.dumps({"erro": "Peso e altura devem ser valores positivos."})

    imc = round(peso / (altura**2), 2)
    categorias = [
        (
            18.5,
            "abaixo do peso",
            "Consulte um especialista para ajustes na sua alimentação.",
        ),
        (
            24.9,
            "peso normal",
            "Continue mantendo hábitos saudáveis!",
        ),
        (
            29.9,
            "sobrepeso",
            "Reavalie sua alimentação e pratique atividades físicas regularmente.",
        ),
        (
            float("inf"),
            "obesidade",
            "Consulte um profissional de saúde para um acompanhamento adequado.",
        ),
    ]

    for limite, estado, recomendacao in categorias:
        if imc <= limite:
            return json.dumps(
                {
                    "imc": imc,
                    "estado": estado,
                    "recomendacao": recomendacao,
                }
            )

    return json.dumps(
        {
            "erro": "Erro inesperado no cálculo do IMC.",
        }
    )


tools = [
    {
        "type": "function",
        "function": {
            "name": "calcular_imc",
            "description": "Calcula o IMC de uma pessoa e fornece uma recomendação de saúde",
            "parameters": {
                "type": "object",
                "properties": {
                    "peso": {
                        "type": "number",
                        "description": "Peso da pessoa em kg",
                    },
                    "altura": {
                        "type": "number",
                        "description": "Altura da pessoa em metros",
                    },
                },
                "required": ["peso", "altura"],
            },
        },
    }
]

funcoes_disponiveis = {"calcular_imc": calcular_imc}

mensagens = [
    {
        "role": "user",
        "content": "Qual é o IMC de uma pessoa que pesa 70 kg e tem 1.75 m de altura?",
    }
]

resposta = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=mensagens,
    tools=tools,
    tool_choice="auto",
)

mensagem_resp = resposta.choices[0].message
print(mensagem_resp)

if tool_calls := mensagem_resp.tool_calls:
    mensagens.append(mensagem_resp)
    for tool_call in tool_calls:
        if function_to_call := funcoes_disponiveis.get(tool_call.function.name):
            function_response = function_to_call(
                **json.loads(tool_call.function.arguments)
            )
            mensagens.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": function_response,
                }
            )

    segunda_resposta = client.chat.completions.create(
        model="gpt-3.5-turbo-0125", messages=mensagens
    )
    print(f"Content: {segunda_resposta.choices[0].message}")
