from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from gemini import googleai_client

llm = googleai_client


class Sentiment(BaseModel):
    """Define o sentimento e o idioma da mensagem enviada"""

    sentimento: str = Field(
        description=(
            "Sentimento do Texto. Deve ser 'positivo', 'negativo' "
            "ou 'neutro' para não definido"
        )
    )
    lingua: str = Field(
        description=(
            "Língua que o texto foi escrito "
            "(deve estar no charset UTF-8)"
        )
    )


texto = "Eu gosto muito de pizza nordestina"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Analise o texto e categorize-o conforme as instruções"),
        ("user", "{input}"),
    ]
)

chain = prompt | llm.bind_tools([Sentiment])

resposta = chain.invoke({"input": texto})
print(resposta)


resposta = chain.invoke({"input": "May the Force be with you"})
print(resposta)
