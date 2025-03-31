from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders import YoutubeAudioLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from gemini import googleai_client
from google_speech_to_text import extrair_audio_youtube, transcrever_audio

llm = googleai_client

url = "https://www.youtube.com/watch?v=ox3-BEfHHnk&t=16s"
save_dir = "files/youtube"

audio_path = extrair_audio_youtube(url)

transcricoes = transcrever_audio(audio_path)

documentos = list(transcricoes)

loader = GenericLoader(YoutubeAudioLoader([url], save_dir), [documentos])

docs = loader.load()
# print(len(documentos))
