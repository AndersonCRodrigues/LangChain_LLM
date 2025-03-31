from langchain_text_splitters import RecursiveCharacterTextSplitter

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

chunk_size = 250
chunk_overlap = 10
char_split = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    separators=[
        "\n\n",
        "\n",
        " ",
        "",
    ],
)

split = char_split.split_text(texto_completo)
print(split)
print(len(split))
