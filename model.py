from faster_whisper import WhisperModel


def Model():
    print("Loading Whisper model...")
    # model = WhisperModel("base", device="cpu", compute_type="int8")
    model = WhisperModel("large-v3", device="cpu", compute_type="int8")
    print("Whisper model loaded!")
    return model
