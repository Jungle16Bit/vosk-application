from vosk import Model, KaldiRecognizer
import wave
import json
import os
import download_audio as dla

# caminho do modelo
model_path_en = "models/vosk-model-small-pt-0.3"

#função para conversão de audio
def convert(audio_in, audio_out):
    os.system(f"ffmpeg -i {audio_in} -ar 16000 -ac 1 -c:a pcm_s16le {audio_out} -y")

#função para transcrição do audio
def transcribe_audio(audio_in ,audio_out, model_path):
    wav_audio = audio_out

    convert(audio_in, wav_audio)

    with wave.open(wav_audio, "rb") as wav:
        if wav.getnchannels() != 1 or wav.getsampwidth() != 2 or wav.getframerate() != 16000:
            raise ValueError("O áudio precisa estar em mono, 16-bit e 16kHz!")

        model = Model(model_path)
        recognizer = KaldiRecognizer(model, wav.getframerate())
        recognizer.SetWords(True)

        text_trasncribe = ""
        while True:
            data_audio = wav.readframes(4000)
            if len(data_audio) == 0:
                break
            if recognizer.AcceptWaveform(data_audio):
                result = json.loads(recognizer.Result())
                text_trasncribe += result.get("text", "") + " "

        result_text = json.loads(recognizer.Result())
        text_trasncribe += result_text.get("text", "")

    os.remove(wav_audio)
    return text_trasncribe.strip()

if __name__ == "__main__":

    #caminho do audio
    audio_path_in = dla.down_ren()
    audio_path_out = "audio/temp.wav"

    text_result = transcribe_audio(audio_path_in, audio_path_out, model_path_en)
    os.system("cls")
    #imprimindo audio transcrito
    print(f"Transcrição: {text_result}")
    os.remove(audio_path_in)
