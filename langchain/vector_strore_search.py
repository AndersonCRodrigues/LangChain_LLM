import warnings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_weaviate import WeaviateVectorStore
from gemini import google_embedding
from weaviate_client import weaviate_client

warnings.simplefilter("ignore", category=DeprecationWarning)

embedding_model = google_embedding
index_name = "documents"

weaviate_store = WeaviateVectorStore(
    client=weaviate_client,
    index_name=index_name,
    embedding=embedding_model,
    text_key="text",
)


def load_and_split_documents(
    file_path="files/apostila.pdf", chunk_size=500, chunk_overlap=50
):
    loader = PyMuPDFLoader(file_path)
    documentos = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(documentos)


def load_documents_if_empty():
    collection = weaviate_client.collections.get(index_name)
    object_count = collection.aggregate.over_all(total_count=True).total_count

    if object_count == 0:
        print("Nenhum documento encontrado. Carregando documentos...")
        documents = load_and_split_documents()
        weaviate_store.add_documents(documents)
    else:
        print(f"{object_count} documentos encontrados no índice.")


def search_and_print_answers(query):
    respostas = weaviate_store.similarity_search(query)
    for resposta in respostas:
        print(resposta.page_content)


def main():
    load_documents_if_empty()

    pergunta = "Quais os principais métodos para manipulação de string?"
    search_and_print_answers(pergunta)


if __name__ == "__main__":
    try:
        main()
    finally:
        weaviate_client.close()
