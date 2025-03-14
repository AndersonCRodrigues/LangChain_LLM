from enum import Enum
import time
from pydantic import BaseModel
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache
from gemini import googleai_client

set_llm_cache(SQLiteCache(database_path="files/vector_store_cache.db"))

llm = googleai_client

solicitacoes = [
    "Meu computador está travando toda vez que tento abrir um programa. "
    "O que devo fazer?",
    "Não consigo acessar minha conta. A senha não está funcionando!",
    "Estou tendo dificuldades para instalar o software de design gráfico. "
    "Pode me ajudar?",
    "Gostaria de saber como atualizar meu endereço de entrega na plataforma.",
    "O meu laptop não está ligando. Acho que é um problema no cabo de " "energia.",
    "Não consigo ver meus arquivos no aplicativo. Existe alguma solução?",
]


class SetorEnum(str, Enum):
    suporte_hardware = "suporte_hardware"
    suporte_software = "suporte_software"
    suporte_conta = "suporte_conta"
    outros = "outros"


class DirecionaSuporte(BaseModel):
    """Direciona a solicitação de suporte para o setor responsável"""

    setor: SetorEnum


system_message = """
Pense com cuidado ao categorizar o texto conforme as instruções.
Questões relacionadas a problemas de hardware, como falha no computador,
laptop ou outros dispositivos físicos devem ser direcionadas para
"suporte_hardware".
Questões relacionadas a problemas com software, como instalação,
erros ao abrir programas, etc., devem ser direcionadas para "suporte_software".
Problemas relacionados ao acesso de conta, como recuperação de senha,
problemas de login, devem ser direcionados para "suporte_conta".
Mensagens que não se encaixam nessas categorias devem ser direcionadas para
"outros".
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_message), ("user", "{input}")]
)

chain = (prompt | llm.bind_tools([DirecionaSuporte])) | JsonOutputFunctionsParser()


for solicitacao in solicitacoes:
    start_time = time.time()
    resposta = chain.invoke({"input": solicitacao})
    elapsed_time = time.time() - start_time
    print(f"Solicitação: {solicitacao}")
    print(f"Resposta: {resposta}")
    print(f"Tempo de resposta: {elapsed_time}")
