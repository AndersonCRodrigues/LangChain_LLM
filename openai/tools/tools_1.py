import json
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.Client()


def saudacao_por_periodo(hora):
    if 5 <= hora < 12:
        return json.dumps({"saudacao": "Bom dia!"})
    elif 12 <= hora < 18:
        return json.dumps({"saudacao": "Boa tarde!"})
    elif 18 <= hora < 22:
        return json.dumps({"saudacao": "Boa noite!"})
    return json.dumps({"saudacao": "Boa madrugada!"})


tools = [
    {
        "type": "function",
        "function": {
            "name": "saudacao_por_periodo",
            "description": "Retorna uma saudação baseada na hora do dia",
            "parameters": {
                "type": "object",
                "properties": {
                    "hora": {
                        "type": "integer",
                        "description": "A hora do dia em formato de 24h",
                    }
                },
                "required": ["hora"],
            },
        },
    }
]

funcao_disponivel = {"saudacao_por_periodo": saudacao_por_periodo}

mensagens = [
    {
        "role": "user",
        "content": "Qual saudação o modelo me dá se for 23h?",
    }
]

resposta = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=mensagens,
    tools=tools,
    tool_choice="auto",
)

mensagem_resp = resposta.choices[0].message
print(f"Mensagem: {mensagem_resp}")

tool_calls = mensagem_resp.tool_calls
print(f"Tools: {tool_calls}")

if tool_calls:
    mensagens.append(mensagem_resp)
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        if function_to_call := funcao_disponivel.get(function_name):
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                hora=function_args.get("hora"),
            )
            mensagens.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

    segunda_resposta = client.chat.completions.create(
        model="gpt-3.5-turbo-0125", messages=mensagens
    )
    mensagem_resposta = segunda_resposta.choices[0].message
    print(f"Content: {mensagem_resposta}")
