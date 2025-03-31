import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_weaviate import WeaviateVectorStore
from gemini import google_embedding
from weaviate_client import weaviate_client


embedding_model = google_embedding
index_name = "project"

weaviate_store = WeaviateVectorStore(
    client=weaviate_client,
    index_name=index_name,
    embedding=embedding_model,
    text_key="text",
)


def list_pdf_files(directory="files"):
    return [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".pdf")
    ]


def load_and_split_documents():
    paths = list_pdf_files()
    paginas = []

    for path in paths:
        loader = PyMuPDFLoader(path)
        paginas.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    documents = splitter.split_documents(paginas)

    for i, doc in enumerate(documents):
        doc.metadata["source"] = doc.metadata["source"].replace("files/", "")
        doc.metadata["doc_id"] = i

    return documents


def load_documents_if_empty():
    collection = weaviate_client.collections.get(index_name)
    object_count = collection.aggregate.over_all(total_count=True).total_count

    if object_count == 0:
        print("Nenhum documento encontrado. Carregando documentos...")
        documents = load_and_split_documents()
        weaviate_store.add_documents(documents)


def search_and_print_answers(query):
    respostas = weaviate_store.max_marginal_relevance_search(
        query,
        k=3,
        fetch_k=10,
    )
    for resposta in respostas:
        print(resposta.page_content)


def main():
    load_documents_if_empty()

    pergunta = "O que é Hugging Face e como faço para acessá-lo?"
    search_and_print_answers(pergunta)


if __name__ == "__main__":
    try:
        main()
    finally:
        weaviate_client.close()
