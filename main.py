import pyaudio
import numpy as np
from model import Model

# Settings
RATE = 16000
CHUNK = 2048  # Increased buffer size to reduce overflow
RECORD_SECONDS = 5  # Process every 5 seconds of audio

model = Model()

print("Starting microphone... Speak in Swedish!")
print("Press Ctrl+C to stop\n")

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK
)

try:
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

        # Convert to numpy array
        audio_data = b"".join(frames)
        audio_np = (
            np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        )

        # Transcribe
        segments, _ = model.transcribe(audio_np, language="sv")

        # Print results
        for segment in segments:
            text = segment.text.strip()
            if text:
                print(f"→ {text}")

except KeyboardInterrupt:
    print("\n\nStopping...")
finally:
    if stream.is_active():
        stream.stop_stream()
    stream.close()
    p.terminate()
