from pydantic import BaseModel, Field
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from gemini import googleai_client

llm = googleai_client

texto = """
A Microsoft foi fundada em 4 de abril de 1975 por Bill Gates e Paul Allen, em
Albuquerque, no estado do Novo México. O nome "Microsoft" é uma combinação das
palavras "microcomputador" e "software", refletindo o foco da empresa em
software
para computadores pessoais. O primeiro grande projeto da Microsoft foi a criação
de um sistema operacional para o computador Altair 8800, um dos primeiros
microcomputadores disponíveis comercialmente. O sistema, denominado Altair BASIC,
foi desenvolvido em parceria com a MITS (Micro Instrumentation and Telemetry
Systems) e foi um marco inicial para a Microsoft. Em 1980, a empresa firmou um
contrato significativo com a IBM para fornecer o sistema operacional para o novo
PC da IBM, o que levou à criação do MS-DOS. Esse contrato foi um ponto de virada
para a Microsoft, impulsionando sua expansão e dominando o mercado de sistemas
operacionais para PCs nos anos seguintes. Com o sucesso do MS-DOS, a Microsoft se
consolidou como líder no setor de software e, em 1985, lançou o Windows, um sistema
operacional gráfico que viria a se tornar a base de sua supremacia no mercado de
sistemas operacionais para desktop.
"""


class Event(BaseModel):
    """Informações sobre um evento ocorrido"""

    date: str = Field(description="Data do evento no formato YYYY-MM-DD")
    event: str = Field(description="Descrição do evento extraído do texto")


class EventsList(BaseModel):
    """Lista de Eventos para Extração"""

    events: List[Event] = Field(
        description="Conjunto de eventos encontrados no texto fornecido"
    )


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Extraia as frases de acontecimentos e as extraia integralmente"),
        ("user", "{input}"),
    ]
)

chain = (prompt | llm.bind_tools([EventsList])) | JsonOutputFunctionsParser()

resposta = chain.invoke({"input": texto})
print(resposta)
