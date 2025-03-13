import warnings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_weaviate import WeaviateVectorStore
from gemini import google_embedding, googleai_client
from weaviate_client import weaviate_client
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache

warnings.simplefilter("ignore", category=DeprecationWarning)
set_llm_cache(SQLiteCache(database_path="files/vector_store_cache.db"))

embedding_model = google_embedding
llm = googleai_client

index_name = "documents"
weaviate_store = WeaviateVectorStore(
    client=weaviate_client,
    index_name=index_name,
    embedding=embedding_model,
    text_key="text",
)


def load_and_split_documents():
    """Carregar e dividir o documento em pedaços menores."""
    loader = PyMuPDFLoader("files/apostila.pdf")
    paginas = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(paginas)


def initialize_qa_chain():
    """Inicializar o fluxo de QA."""
    retriever = weaviate_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="refine",
        retriever=retriever,
        return_source_documents=True,
    )


def handle_question(qa_chain, question):
    """Processar uma pergunta e obter a resposta."""
    prompt_template = PromptTemplate(
        input_variables=["pergunta"],
        template="""
        Responda a seguinte pergunta de forma clara,
        dando exemplos do documento,
        de objetiva em português: {pergunta}
        """,
    )
    prompt_formatado = prompt_template.format(pergunta=question)
    return qa_chain.invoke(prompt_formatado)["result"]


def main():
    collection = weaviate_client.collections.get(index_name)
    object_count = collection.aggregate.over_all(total_count=True).total_count

    if object_count == 0:
        print("Nenhum documento encontrado. Carregando novamente...")
        documents = load_and_split_documents()
        weaviate_store.add_documents(documents)

    qa_chain = initialize_qa_chain()
    pergunta = "Quais os principais métodos para manipulação de string?"

    resposta = handle_question(qa_chain, pergunta)
    print(resposta)


if __name__ == "__main__":
    try:
        main()
    finally:
        weaviate_client.close()
