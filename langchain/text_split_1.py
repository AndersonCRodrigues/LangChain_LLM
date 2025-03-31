import string
from langchain_text_splitters import CharacterTextSplitter

texto_completo = """
Python é uma linguagem de programação de alto nível conhecida por sua simplicidade,
legibilidade e versatilidade. Seu design foi criado com o objetivo de ser fácil de
aprender e usar, permitindo que programadores escrevam código de maneira mais
intuitiva e eficiente. Ao contrário de outras linguagens, Python prioriza a
legibilidade do código, o que facilita a compreensão e manutenção do software,
mesmo por programadores que não são os autores do código original.
Sua sintaxe clara, por exemplo, elimina a necessidade de muitos símbolos ou
palavras-chave complicadas, tornando o código mais próximo da linguagem humana.
"""

chunk_size = 50
chunk_overlap = 0
char_split = CharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator=""
)

texto = "".join(f"{string.ascii_lowercase}" for _ in range(5))

split = char_split.split_text(texto)
print(split)
print(len(split))

split = char_split.split_text(texto_completo)
print(split)
print(len(split))
