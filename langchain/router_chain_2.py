from gemini import googleai_client
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import (
    RunnableLambda,
    RunnableMap,
)


llm = googleai_client

quimica_template = ChatPromptTemplate.from_template(
    """Você é um químico experiente, especializado em explicar conceitos de
química de forma clara e objetiva. Seu conhecimento abrange reações químicas,
elementos, compostos e a relação entre estrutura molecular e propriedades dos
materiais. Se não souber a resposta para uma pergunta, você admite isso.

Pergunta: {input}"""
)

geografia_template = ChatPromptTemplate.from_template(
    """Você é um geógrafo com amplo conhecimento sobre processos naturais,
geografia humana, clima, relevo e a interação entre ambiente e sociedade.
Você explica como fatores físicos e humanos moldam o mundo ao nosso redor
de maneira acessível e precisa.

Pergunta: {input}"""
)

biologia_template = ChatPromptTemplate.from_template(
    """Você é um biólogo altamente capacitado, com expertise em seres vivos,
suas estruturas, funções e interações ecológicas. Você é excelente em tornar
conceitos biológicos compreensíveis tanto para iniciantes quanto para
especialistas.

Pergunta: {input}"""
)

prompt_infos = {
    "Química": {
        "description": "Ideal para perguntas de química",
        "prompt": quimica_template,
    },
    "Geografia": {
        "description": "Ideal para perguntas de geografia",
        "prompt": geografia_template,
    },
    "Biologia": {
        "description": "Ideal para perguntas de biologia",
        "prompt": biologia_template,
    },
}


def determinar_destino(input_text):
    if "química" in input_text.lower():
        return "Química"
    elif "geografia" in input_text.lower():
        return "Geografia"
    elif "biologia" in input_text.lower():
        return "Biologia"
    else:
        return "Padrão"


default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = default_prompt | llm

chains_destino = {
    nome: (info["prompt"] | llm)
    for nome, info in prompt_infos.items()
    }

selecionar_cadeia = RunnableLambda(
    lambda input_text: chains_destino.get(
        determinar_destino(input_text),
        default_chain,
    )
)

pipeline = selecionar_cadeia | RunnableMap({"input": lambda x: x})


input_text = "O que é o El Niño?"
resposta = pipeline.invoke(input_text)
print(resposta)
