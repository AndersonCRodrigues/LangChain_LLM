from langchain_community.document_loaders import PyMuPDFLoader
from langchain.chains.question_answering import load_qa_chain
from gemini import googleai_client

llm = googleai_client

arquivo = "files/apostila.pdf"
loader = PyMuPDFLoader(arquivo)
documentos = loader.load()
# print(len(documentos))

chain = load_qa_chain(
    llm=llm,
    chain_type="stuff",
    verbose=True,
)
pergunta = "Do que se trata esse documento?"
resposta = chain.run(input_documents=documentos[:8], question=pergunta)
print(resposta)
