import pyaudio

RATE = 16000
CHUNK = 2048


def MicrophoneStream():
    print("Startar mikrofonen... Prata på svenska!")
    print("Tryck Ctrl+C för att sluta\n")

    p = pyaudio.PyAudio()
    return p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
