from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langgraph.prebuilt import create_react_agent
from gemini import googleai_client


llm = googleai_client


def resposta_simples(query: str) -> str:
    return f"A resposta para a '{query}' é Paris!"


tools = [
    Tool(
        name="resposta_simples",
        func=resposta_simples,
        description="Uma ferramenta simples para respostas diretas.",
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

langgraph_agent_executor = create_react_agent(
    model=llm,
    tools=tools,
)


input_query = "Qual é a capital da França?"
# resposta = agent.invoke(input_query)
response = langgraph_agent_executor.invoke(
    {
        "messages": [{"role": "human", "content": input_query}],
    }
)
print(response)
