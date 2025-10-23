import numpy as np
from model import Model
from recorder import Recorder
from datetime import datetime
import os


class Transcriber:
    def __init__(self, recording_filename, transcription_filename):
        self.transcription_filename = transcription_filename
        self.recording_filename = recording_filename
        self.model = Model()

    def save(self):
        with open(self.recording_filename, "rb") as recording_file:
            all_audio_data = recording_file.read()

        # Convert to numpy array for transcription
        audio_np = (
            np.frombuffer(all_audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        )

        segments, _info = self.model.transcribe(audio_np, language="sv")

        with open(
            self.transcription_filename, "w", encoding="utf-8"
        ) as transcription_file:
            for segment in segments:
                text = segment.text.strip()
                if text:
                    content = f"{segment.start}-{segment.end}>{segment.text}"
                    print(content)
                    transcription_file.write(content + "\n")


def main():
    print("Startar mikrofonen... Prata på svenska!")
    print("Tryck Enter för att sluta spela in och börja transkriberingen.")

    os.makedirs("recordings", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recording_filename = f"recordings/{timestamp}.raw"

    recorder = Recorder(recording_filename)
    recorder.start()

    try:
        input()
        print("\nStopping recording...")
        recorder.stop()

        print("Transcribing audio...\n")
        transcription_filename = f"recordings/{timestamp}.txt"
        transcriber = Transcriber(recording_filename, transcription_filename)
        transcriber.save()
        print("Transcription saved!")

    except Exception as e:
        print(f"Error: {e}")


main()
