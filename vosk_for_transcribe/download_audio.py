import os

def down_ren():
    path = "audio/"
    url =  input(str("url do video: "))

    output_path = os.path.join(path, "%(title)s.%(ext)s")
    os.system(f'yt-dlp -f bestaudio -x --audio-format wav --postprocessor-args "ffmpeg:-ac 1" -o "{output_path}" {url}')

    archives = os.listdir(path)

    if archives:
        old_arch_path = os.path.join(path, archives[0])

        arch_new_name = "audio_transcribe.wav"
        new_arch_path = os.path.join(path, arch_new_name)

        os.rename(old_arch_path, new_arch_path)
        
        return new_arch_path; print(f"baixou essa caralha aqui: {old_arch_path}")
    else:
        print("Nenhum arquivo encontrado para renomear.")

if __name__ == "__main__":
    down_ren()