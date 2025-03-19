import pandas as pd
from langchain_experimental.agents.agent_toolkits import (
    create_pandas_dataframe_agent,
)
from gemini import googleai_client

df_temp = pd.read_csv("https://datahub.io/core/global-temp/r/0.csv")
# print(df_temp.head())

print()
llm = googleai_client


agent_temp = create_pandas_dataframe_agent(
    llm=llm,
    df=df_temp,
    verbose=True,
    agent_type="tool-calling",
    allow_dangerous_code=True,
)

# 1- Calcule a temperatura média global para o ano mais recente.
resposta = agent_temp.invoke(
    {
        "input": "Calcule a temperatura média global para o ano mais recente.",
    }
)
print(resposta)

# 2- QUal foi o ano com a maior temperatura média?
resposta = agent_temp.invoke(
    {
        "input": "Qual foi o ano com maior temperatura média?",
    }
)
print(resposta)
