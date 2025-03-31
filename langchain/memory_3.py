from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationTokenBufferMemory
from gemini import googleai_client

llm = googleai_client

# Gemini não suporta max token limit
memory = ConversationTokenBufferMemory(
    llm=llm,
)
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True,
)

conversation.predict(input="Faça uma poesia de 400 palavras")
print(conversation.predict(input="Resuma a poesia anterior"))
