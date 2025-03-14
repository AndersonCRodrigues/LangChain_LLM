from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.llm import LLMChain
from gemini import googleai_client

llm = googleai_client

prompt = ChatPromptTemplate.from_template("Crie uma frase sobre: {assunto}")

chain = prompt | llm

# resposta = chain.invoke({"assunto": "Python"})
# print(resposta)


output_parser = StrOutputParser()

chain = prompt | llm | output_parser
resposta = chain.invoke({"assunto": "Python"})
print(resposta)

quest = {"assunto": "Python"}

prompt_format = prompt.invoke(quest)
print(prompt_format)

resposta = llm.invoke(prompt_format)
print(resposta)

prompt = ChatPromptTemplate.from_template(
    "Crie uma frase sobre o assunto {assunto}",
)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
    output_parser=output_parser,
)

resposta = chain.invoke({"assunto": "Python"})
print(resposta)
