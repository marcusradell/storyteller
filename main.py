import numpy as np
from model import Model
from microphone_stream import MicrophoneStream, CHUNK
from datetime import datetime
import os


def main():
    # Create recordings directory if it doesn't exist
    os.makedirs("recordings", exist_ok=True)

    # Generate timestamp-based filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recording_file = f"recordings/{timestamp}.raw"
    transcription_file = f"recordings/{timestamp}.txt"

    model = Model()
    microphone_stream = MicrophoneStream()

    print(f"Recording to: {recording_file}")
    print("Press Ctrl+C to stop recording and transcribe...\n")

    try:
        with open(recording_file, "wb") as f:
            while True:
                try:
                    audio_data = microphone_stream.read(CHUNK)
                    f.write(audio_data)
                    f.flush()  # Ensure data is written to disk
                    print(".", end="", flush=True)  # Progress indicator
                except OSError:
                    print("Warning: Audio buffer overflow, skipping frame")
                    continue

    except KeyboardInterrupt:
        print("\n\nStopping recording...")
        print("Transcribing audio...\n")

        # Read the recorded audio from file for transcription
        with open(recording_file, "rb") as f:
            all_audio_data = f.read()

        # Convert to numpy array for transcription
        audio_np = (
            np.frombuffer(all_audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        )

        # Transcribe
        segments, _ = model.transcribe(audio_np, language="sv")

        # Print results and save to file
        print("\nTranscription:")
        print("-" * 50)

        with open(transcription_file, "w", encoding="utf-8") as f:
            for segment in segments:
                text = segment.text.strip()
                if text:
                    print(f"→ {text}")
                    f.write(f"{text}\n")

        print("-" * 50)
        print(f"\nRecording saved to: {recording_file}")
        print(f"Transcription saved to: {transcription_file}")


main()
