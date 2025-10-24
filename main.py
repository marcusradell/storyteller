from recorder import Recorder
from transcriber import Transcriber
from datetime import datetime
import os


def main():
    print("Startar mikrofonen...")
    print("Tryck Enter för att sluta spela in och påbörja transkriberingen.")

    os.makedirs("recordings", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recording_filename = f"recordings/{timestamp}.raw"

    recorder = Recorder(recording_filename)
    recorder.start()

    input()
    print("\nStopping recording...")
    recorder.stop()

    print("Transcribing audio...\n")
    transcription_filename = f"recordings/{timestamp}.txt"
    transcriber = Transcriber(recording_filename, transcription_filename)
    transcriber.save()
    print("Transcription saved!")


main()
