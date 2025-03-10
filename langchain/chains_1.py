from gemini import googleai_client
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain

llm = googleai_client

memory = ConversationBufferMemory()
chain = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True,
)

print(chain.predict(input="Olá"))
