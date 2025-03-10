from gemini import googleai_client
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain

llm = googleai_client

prompt_template = PromptTemplate.from_template(
    """
Essa é uma conversa amigável entre um humano e uma IA

Conversa atual:
{history}
Human: {input}
AI:
"""
)

memory = ConversationBufferMemory()

chain = ConversationChain(
    prompt=prompt_template,
    llm=llm,
    memory=memory,
    verbose=True,
)

response = chain.predict(input="Oi")
print(response)
