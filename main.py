import numpy as np
from model import Model
from microphone_stream import MicrophoneStream, RATE, CHUNK, RECORD_SECONDS
from datetime import datetime
import os

# Create recordings directory if it doesn't exist
os.makedirs("recordings", exist_ok=True)

# Generate timestamp-based filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
recording_file = f"recordings/{timestamp}.raw"

model = Model()
stream = MicrophoneStream()

print(f"Recording to: {recording_file}")
print("Press Ctrl+C to stop recording and transcribe...\n")

all_audio_data = b""

try:
    with open(recording_file, "wb") as f:
        while True:
            # Record audio chunk
            frames = []
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames.append(data)
                except OSError as e:
                    print(f"Warning: Audio buffer overflow, skipping frame")
                    continue

            # Convert to binary data and save
            audio_data = b"".join(frames)
            f.write(audio_data)
            f.flush()  # Ensure data is written to disk
            all_audio_data += audio_data
            print(".", end="", flush=True)  # Progress indicator

except KeyboardInterrupt:
    print("\n\nStopping recording...")
    print("Transcribing audio...\n")
    
    # Convert to numpy array for transcription
    audio_np = (
        np.frombuffer(all_audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    )

    # Transcribe
    segments, _ = model.transcribe(audio_np, language="sv")

    # Print results
    print("\nTranscription:")
    print("-" * 50)
    for segment in segments:
        text = segment.text.strip()
        if text:
            print(f"→ {text}")
    print("-" * 50)
    print(f"\nRecording saved to: {recording_file}")
