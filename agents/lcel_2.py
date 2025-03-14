from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_weaviate import WeaviateVectorStore
from gemini import google_embedding, googleai_client
from weaviate_client import weaviate_client
from langchain_community.cache import SQLiteCache
from langchain.globals import set_llm_cache
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

cache = SQLiteCache(database_path="files/vector_store_cache.db")

set_llm_cache(cache)

embedding_model = google_embedding
llm = googleai_client

index_name = "lcel"
weaviate_store = WeaviateVectorStore(
    client=weaviate_client,
    index_name=index_name,
    embedding=embedding_model,
    text_key="text",
)


def list_pdf_files():
    return ["files/LLM.pdf"]


def load_and_split_documents():
    paths = list_pdf_files()
    paginas = [page for path in paths for page in PyMuPDFLoader(path).load()]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    documents = splitter.split_documents(paginas)

    for i, doc in enumerate(documents):
        doc.metadata.update(
            {
                "source": doc.metadata["source"].replace("files/", ""),
                "doc_id": i,
            }
        )

    return documents


def check_existing_documents():
    collection = weaviate_client.collections.get(index_name)
    return collection.aggregate.over_all(total_count=True).total_count


if check_existing_documents() == 0:
    print("Nenhum documento encontrado. Carregando novamente...")
    new_documents = load_and_split_documents()
    weaviate_store.add_documents(new_documents)

template_str = """
        Responda as perguntas do usuário com base no contexto fornecido.
        Contexto: {contexto}
        Pergunta: {pergunta}
        """
template = ChatPromptTemplate.from_template(template_str)
output_parser = StrOutputParser()

retriever = weaviate_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3},
)

setup_retrieval = RunnableParallel(
    {"pergunta": RunnablePassthrough(), "contexto": retriever}
)
chain = setup_retrieval | template | llm | output_parser

try:
    resposta = chain.invoke("O que é LLM?")
    print(resposta)

finally:
    weaviate_client.close()
