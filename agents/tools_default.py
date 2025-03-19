from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain_community.agent_toolkits.load_tools import load_tools


tool_repl = PythonAstREPLTool()
# print(tool_repl.description)

tools = load_tools(["stackexchange"])

tools_stack = tools[0]

print(tools_stack.run({"query": "Langchain"}))
