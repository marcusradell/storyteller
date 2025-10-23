import pyaudio

CHUNK = 1024


def MicrophoneStream():
    p = pyaudio.PyAudio()
    return p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=CHUNK,
    )
