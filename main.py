import numpy as np
from model import Model
from recording import Recording
from datetime import datetime
import os
import threading


def stop_recording_on_enter(stop_event, recording_thread):
    # Wait for user to press Enter
    stop_event.set()
    recording_thread.join()


def save_transcription(recording_filename, transcription_filename):
    with open(recording_filename, "rb") as recording_file:
        all_audio_data = recording_file.read()

    # Convert to numpy array for transcription
    audio_np = (
        np.frombuffer(all_audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    )

    model = Model()
    segments, _info = model.transcribe(audio_np, language="sv")

    with open(transcription_filename, "w", encoding="utf-8") as transcription_file:
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

    recording = Recording(recording_filename)
    recording.start()

    try:
        input()
        print("\nStopping recording...")
        recording.stop()

        print("Transcribing audio...\n")
        transcription_file = f"recordings/{timestamp}.txt"
        save_transcription(recording_filename, transcription_file)
        print("Transcription saved!")

    except Exception as e:
        print(f"Error: {e}")


main()
