import numpy as np
from model import Model
from microphone_stream import MicrophoneStream, CHUNK
from datetime import datetime
import os


def record_audio_stream(recording_file):
    microphone_stream = MicrophoneStream()

    with open(recording_file, "wb") as f:
        while True:
            audio_data = microphone_stream.read(CHUNK)
            f.write(audio_data)
            f.flush()


def save_transcription(recording_file, transcription_file):
    with open(recording_file, "rb") as f:
        all_audio_data = f.read()

    # Convert to numpy array for transcription
    audio_np = (
        np.frombuffer(all_audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    )

    model = Model()
    segments, _info = model.transcribe(audio_np, language="sv")

    with open(transcription_file, "w", encoding="utf-8") as f:
        for segment in segments:
            text = segment.text.strip()
            if text:
                content = f"{segment.start}-{segment.end}>{segment.text}"
                print(content)
                f.write(content + "\n")


def main():
    print("Startar mikrofonen... Prata på svenska!")
    print("Tryck Ctrl+C för att sluta spela in och börja transkriberingen.")

    os.makedirs("recordings", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recording_file = f"recordings/{timestamp}.raw"

    try:
        record_audio_stream(recording_file)
    except KeyboardInterrupt:
        print("Transcribing audio...\n")

        transcription_file = f"recordings/{timestamp}.txt"
        save_transcription(recording_file, transcription_file)

        print("Transcription saved!")
    except Exception as e:
        print(f"Error: {e}")


main()
