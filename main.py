from recorder import Recorder
from transcriber import Transcriber
from datetime import datetime
import os
import signal
import sys
import threading


def main():
    print("Startar mikrofonen...")
    print("Tryck Ctrl+C för att sluta spela in och påbörja transkriberingen.")

    os.makedirs("recordings", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recording_filename = f"recordings/{timestamp}.raw"

    recorder = Recorder(recording_filename)
    recorder.start()

    stop_event = threading.Event()

    def signal_handler(sig, frame):
        print("\nStopping recording...")
        recorder.stop()
        print("Transcribing audio...\n")
        transcription_filename = f"recordings/{timestamp}.txt"
        transcriber = Transcriber(recording_filename, transcription_filename)
        transcriber.save()
        print("Transcription saved!")
        stop_event.set()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("Recording... (Press Ctrl+C to stop)")
    stop_event.wait()


main()
