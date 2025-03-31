from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from gemini import googleai_client

llm = googleai_client

memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

conversation.predict(input="Olá, meu nome é Anderson")
conversation.predict(input="Como vai?")
print(conversation.predict(input="Qual é o meu nome?"))
