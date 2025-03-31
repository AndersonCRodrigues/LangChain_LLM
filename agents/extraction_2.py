from langchain_community.document_loaders.web_base import WebBaseLoader
from pydantic import BaseModel, Field
from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from gemini import googleai_client

llm = googleai_client

loader = WebBaseLoader("https://www.techtudo.com.br")
page = loader.load()
# print(page)


class BlogPost(BaseModel):
    """Detalhes sobre uma postagem de blog"""

    title: str = Field(description="Título da postagem no blog")
    author: str = Field(description="Nome do autor da postagem no blog")


class BlogSite(BaseModel):
    """Conjunto de postagens de blog de um site específico"""

    posts: List[BlogPost] = Field(
        description="Coleção de postagens de blog do site",
    )


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Extraia da página os posts do blog "
            "com as informações especificadas. "
            "Traga as cinco primeira informações",
        ),
        ("user", "{input}"),
    ]
)

chain = prompt | llm.bind_tools([BlogSite]) | JsonOutputFunctionsParser()
resposta = chain.invoke({"input": page})
print(resposta)
