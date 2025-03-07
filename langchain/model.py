from gemini import googleai_client

llm = googleai_client
prompt = "Conte uma história sobre aprendizado de máquina"
response = llm.invoke(prompt)

print(response.content)

for trecho in llm.stream(prompt):
    print(trecho.content, end="")
