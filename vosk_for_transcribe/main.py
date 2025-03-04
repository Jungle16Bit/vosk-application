from vosk import Model, KaldiRecognizer
import wave
import json
import os
import download_audio as dla

# caminho do modelo
model_path = r"vosk_for_transcribe/models/vosk-model-small-pt-0.3"

#função para transcrição do audio
def transcribe_audio(audio, model_path):

    with wave.open(audio, "rb") as wav:
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

    return text_trasncribe.strip()

if __name__ == "__main__":

    #caminho do audio
    audio = dla.run()
    text_result = transcribe_audio(audio, model_path)
    os.system("cls")
    #imprimindo audio transcrito
    print(f"Transcrição: {text_result}")
    os.remove(audio)
