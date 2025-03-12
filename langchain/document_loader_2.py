from langchain_community.document_loaders import CSVLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from gemini import googleai_client

llm = googleai_client

arquivo = "files/imdb_movies.csv"
loader = CSVLoader(arquivo)
documentos = loader.load()
# print(len(documentos))

prompt = ChatPromptTemplate.from_template(
    "Qual filme com menor e maior metascore, em português?: {context}"
)
chain = create_stuff_documents_chain(llm, prompt)

resposta = chain.invoke({"context": documentos[:10]})
print(resposta)
