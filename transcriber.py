from model import Model
import numpy as np


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
