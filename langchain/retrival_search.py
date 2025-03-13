import os
import warnings
import time
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_weaviate import WeaviateVectorStore
from gemini import google_embedding, googleai_client
from weaviate_client import weaviate_client
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache

warnings.simplefilter("ignore", category=DeprecationWarning)
set_llm_cache(SQLiteCache(database_path="files/vector_store_cache.db"))

embedding_model = google_embedding
llm = googleai_client

index_name = "new_documents"
weaviate_store = WeaviateVectorStore(
    client=weaviate_client,
    index_name=index_name,
    embedding=embedding_model,
    text_key="text",
)


def list_pdf_files(directory="files"):
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(".pdf")
    ]


def load_and_split_documents():
    paths = list_pdf_files()
    paginas = []

    for path in paths:
        loader = PyMuPDFLoader(path)
        paginas.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    documents = splitter.split_documents(paginas)

    for i, doc in enumerate(documents):
        doc.metadata["source"] = doc.metadata["source"].replace("files/", "")
        doc.metadata["doc_id"] = i

    return documents


def initialize_qa_chain():
    retriever = weaviate_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},
    )

    system_prompt = (
        "Use o contexto fornecido para responder à pergunta. "
        "Se não souber a resposta, diga que não sabe. "
        "Contexto: {context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, question_answer_chain)


def handle_question(chain, question):
    return chain.invoke({"input": question})["answer"]


def check_existing_documents():
    collection = weaviate_client.collections.get(index_name)
    return collection.aggregate.over_all(total_count=True).total_count


def main():
    if check_existing_documents() == 0:
        print("Nenhum documento encontrado. Carregando novamente...")
        new_documents = load_and_split_documents()
        weaviate_store.add_documents(new_documents)

    start_time = time.time()
    qa_chain = initialize_qa_chain()
    pergunta = "O que é LLM?"
    resposta = handle_question(qa_chain, pergunta)
    print(resposta)
    elapsed_time = time.time() - start_time

    if elapsed_time < 1:
        print("✅ Resposta veio do cache!")
    else:
        print("❌ LLM foi chamado!")


if __name__ == "__main__":
    try:
        main()
    finally:
        weaviate_client.close()
