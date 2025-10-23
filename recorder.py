import pyaudio
import threading


class Recorder:
    def __init__(self, filename):
        self.filename = filename
        self.recording_thread = None
        self.frames_per_buffer = 1024
        self.pyAudio = pyaudio.PyAudio()
        self.stop_event = threading.Event()

    def _open_stream(self):
        return self.pyAudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=self.frames_per_buffer,
        )

    def _record_audio_stream(self):
        microphone_stream = self._open_stream()

        with open(self.filename, "wb") as file:
            while not self.stop_event.is_set():
                audio_data = microphone_stream.read(self.get_frames_per_buffer())
                file.write(audio_data)

        microphone_stream.close()

    def get_frames_per_buffer(self):
        return self.frames_per_buffer

    def get_filename(self):
        return self.filename

    def stop(self):
        self.stop_event.set()
        self.recording_thread.join()

    def start(self):
        self.recording_thread = threading.Thread(target=self._record_audio_stream)
        self.recording_thread.start()
