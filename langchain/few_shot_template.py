from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from gemini import googleai_client

llm = googleai_client

exemplos = [
    {
        "pergunta": "Qual é a maior montanha do mundo, o Monte Everest ou o K2?",
        "resposta": """São necessárias perguntas de acompanhamento aqui: Sim.
Pergunta de acompanhamento: Qual é a altura do Monte Everest?
Resposta intermediária: O Monte Everest tem 8.848 metros de altura.
Pergunta de acompanhamento: Qual é a altura do K2?
Resposta intermediária: O K2 tem 8.611 metros de altura.
Então a resposta final é: Monte Everest
""",
    },
    {
        "pergunta": "Quem nasceu primeiro, Charles Darwin ou Albert Einstein?",
        "resposta": """São necessárias perguntas de acompanhamento aqui: Sim.
Pergunta de acompanhamento: Quando nasceu Charles Darwin?
Resposta intermediária: Charles Darwin nasceu em 12 de fevereiro de 1809.
Pergunta de acompanhamento: Quando nasceu Albert Einstein?
Resposta intermediária: Albert Einstein nasceu em 14 de março de 1879.
Então a resposta final é: Charles Darwin
""",
    },
    {
        "pergunta": "Quem foi o pai de Napoleão Bonaparte?",
        "resposta": """São necessárias perguntas de acompanhamento aqui: Sim.
Pergunta de acompanhamento: Quem foi Napoleão Bonaparte?
Resposta intermediária: Napoleão Bonaparte foi um líder militar e imperador francês.
Pergunta de acompanhamento: Quem foi o pai de Napoleão Bonaparte?
Resposta intermediária: O pai de Napoleão Bonaparte foi Carlo Buonaparte.
Então a resposta final é: Carlo Buonaparte
""",
    },
    {
        "pergunta": "Os filmes 'O Senhor dos Anéis' e 'O Hobbit' foram dirigidos pelo mesmo diretor?",
        "resposta": """São necessárias perguntas de acompanhamento aqui: Sim.
Pergunta de acompanhamento: Quem dirigiu 'O Senhor dos Anéis'?
Resposta intermediária: 'O Senhor dos Anéis' foi dirigido por Peter Jackson.
Pergunta de acompanhamento: Quem dirigiu 'O Hobbit'?
Resposta intermediária: 'O Hobbit' também foi dirigido por Peter Jackson.
Então a resposta final é: Sim
""",
    },
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{pergunta}"),
        ("ai", "{resposta}"),
    ]
)

few_shot_template = FewShotChatMessagePromptTemplate(
    examples=exemplos,
    example_prompt=example_prompt,
)

prompt_final = ChatPromptTemplate.from_messages(
    [few_shot_template, ("human", "{input}")]
)


prompt = prompt_final.format_messages(
    input="Quem fez mais gols, Messi ou Cristiano Ronaldo?"
)

print(prompt)

chat = llm.invoke(prompt)
print(chat.content)
