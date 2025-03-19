from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from gemini import googleai_client

db_sakila = SQLDatabase.from_uri("sqlite:///files/sakila_master.db")
llm = googleai_client

agent_executor_sakila = create_sql_agent(
    llm=llm,
    db=db_sakila,
    agent_type="tool-calling",
    verbose=True,
)
pergunta = "Quais os 10 filmes mais alugados com a quantidade de alugues de cada um?"
resposta = agent_executor_sakila.invoke(pergunta)
print(resposta)

pergunta = "Quais o nome dos atores atuaram em mais filmes e a quantidade?"
resposta = agent_executor_sakila.invoke(pergunta)
print(resposta)
