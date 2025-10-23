import pyaudio
import numpy as np
from faster_whisper import WhisperModel

# Settings
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5  # Process every 5 seconds of audio

print("Loading Whisper model...")
model = WhisperModel("base", device="cpu", compute_type="int8")
print("Whisper model loaded!")

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
            data = stream.read(CHUNK)
            frames.append(data)

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
    stream.stop_stream()
    stream.close()
    p.terminate()
