import sqlite3
from langgraph.prebuilt import create_react_agent
from langchain.tools import Tool
from gemini import googleai_client


llm = googleai_client


def create_database():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute(
        """
              CREATE TABLE users
              (id INTEGER PRIMARY KEY, name TEXT, age INTEGER
              )
        """
    )
    c.execute("INSERT INTO users (name, age) VALUES " "('João', 25), ('Maria', 30)")
    conn.commit()
    return conn


def search_user_db(user_name):
    conn = create_database()
    c = conn.cursor()
    c.execute("SELECT name, age FROM users WHERE name = ?", (user_name,))
    result = c.fetchone()
    conn.close()
    if result:
        return f"{result[0]} tem {result[1]} anos"
    else:
        return "Usuário não encontrado"


def sum_numbers(numbers):
    if isinstance(numbers, str):
        numbers = eval(numbers)

    if isinstance(numbers, list):
        total = sum(numbers)
        return f"A soma dos números {numbers} é {total}"
    else:
        return "Erro: A entrada não é uma lista de números válida."


tools = [
    Tool(
        name="buscar_usuario_no_db",
        func=search_user_db,
        description="Procura informações sobre um usuário na base de dados",
    ),
    Tool(
        name="calcular_soma",
        func=sum_numbers,
        description="Calcula a soma de uma lista de números",
    ),
]

langgraph_agent_executor = create_react_agent(
    model=llm,
    tools=tools,
)

input_query = "Qual é a soma de 5, 10 e 15? Quantos anos Maria tem?"
response = langgraph_agent_executor.invoke(
    {
        "messages": [("human", input_query)],
    }
)
print(response)
