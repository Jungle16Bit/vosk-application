import yt_dlp
import ffmpeg
import re
import os

file_name = ""

# função para capturar o nome do arquivo que foi baixado
def post_process(d):
    global file_name
    file_name = d["filename"]
    print(f"\n[NOME DO ARQUIVO]: {file_name}.\n")

#configuração para baixar o video.
#OBS: como eu não encontrei nenhuma documentação detalhada a conversão final fica pelo ffmpeg.
ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "vosk_for_transcribe/audio/%(title)s.%(ext)s",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }
    ],
    "progress_hooks": [post_process]
}

# função para converter o arquivo baixado em determinadas especificações
def convert(archive, archive_out):
    try:
        ffmpeg.input(archive).output(archive_out, ac=1, ar='16000', acodec="pcm_s16le", loglevel="error").run()
    except ffmpeg.Error as e:
        print(f"Erro: {e}")
        return None
    return archive

#função de download
def download(url, dl_opts):
    with yt_dlp.YoutubeDL(dl_opts) as ydl:
        ydl.download([url])

def run():
    # url do video que será baixado
    link_url = input("url: ")

    #chama a função de download
    download(link_url, ydl_opts); print(f"[DEBUG] {file_name}")

    #como aqui ele usa o nome do arquivo que foi baixado e no pós-processamento convertemos ele para .wav, o nome está desatualizado.
    file_in = file_name.replace(".webm", ".wav")

    # Verificando o caminho absoluto
    file_name_abs = os.path.abspath(file_in)

    caminho, ext = os.path.splitext(file_name_abs)
    file_safe_abs = caminho + "[output]" + ext

    print(f"[DEBUG] Caminho Absoluto de Entrada: {file_name_abs}")
    print(f"[DEBUG] Caminho Absoluto de Saída: {file_safe_abs}")

    convert(file_name_abs, file_safe_abs)

    try:
        os.remove(file_name_abs)
    except:
        pass

    return file_safe_abs