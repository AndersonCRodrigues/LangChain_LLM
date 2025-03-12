import whisper
from pytube import YouTube
import os

# Carregar o modelo Whisper
modelo = whisper.load_model("base")


# Função para transcrever áudio com Whisper
def transcrever_audio(arquivo_audio):
    # Transcrever o áudio usando o modelo Whisper
    resultado = modelo.transcribe(arquivo_audio, language="pt")

    return [resultado["text"]]


# Função para extrair o áudio de um vídeo do YouTube
def extrair_audio_youtube(url, save_dir="audio_files"):
    yt = YouTube(url)
    # Extrai o áudio em formato mp4
    stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
    caminho_audio = os.path.join(save_dir, f"{yt.title}.mp4")
    # Baixa o áudio para o diretório especificado
    stream.download(output_path=save_dir, filename=f"{yt.title}.mp4")
    return caminho_audio
