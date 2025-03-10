from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)
memory.chat_memory.add_user_message("Olá")
memory.chat_memory.add_ai_message("Como vai?")
print(memory.load_memory_variables({}))
