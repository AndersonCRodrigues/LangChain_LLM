from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

arquivo = "files/apostila.pdf"
loader = PyMuPDFLoader(arquivo)
documentos = loader.load()

chunk_size = 50
chunk_overlap = 10
char_split = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
)

split = char_split.split_documents(documentos)
print(len(split))
