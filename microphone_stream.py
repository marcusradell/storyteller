import pyaudio

CHUNK = 1024


def MicrophoneStream():
    print("Startar mikrofonen... Prata på svenska!")
    print("Tryck Ctrl+C för att sluta\n")

    p = pyaudio.PyAudio()
    return p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=CHUNK,
    )
