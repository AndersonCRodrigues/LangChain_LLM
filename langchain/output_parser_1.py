from langchain.prompts import ChatPromptTemplate
from gemini import googleai_client

llm = googleai_client

feedback_produto = """
Estou muito satisfeito com o Smartphone XYZ Pro. O desempenho é excelente, e o sistema
operacional é rápido e intuitivo. A câmera é um dos principais destaques, especialmente o
modo noturno, que captura imagens incríveis mesmo em baixa iluminação. A duração da bateria
também impressiona, durando facilmente um dia inteiro com uso intenso.
Por outro lado, sinto que o produto poderia ser melhorado em alguns aspectos. A tela,
embora tenha cores vibrantes, parece refletir bastante luz, dificultando o uso sob o sol.
Além disso, o carregador incluído na caixa não oferece carregamento rápido, o que é um ponto
negativo considerando o preço do aparelho
"""

review_template = ChatPromptTemplate.from_template(
    """
Para o texto a seguir, extraia as seguintes informações:
produto: Nome do produto mencionado no texto.
características_positivas: Liste todas as características positivas mencionadas sobre o produto.
características_negativas: Liste todas as características negativas mencionadas sobre o produto.
recomendação: O cliente recomenda o produto? Responda True para sim ou False para não.

Texto: {review}

Retorne a resposta no formato JSON
"""
)

resposta = llm.invoke(review_template.format_messages(review=feedback_produto))

print(resposta.content)
