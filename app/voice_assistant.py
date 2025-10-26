import pyttsx3
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import os
import threading

# ---- Vosk Model Path ----
VOSK_MODEL_PATH = r"E:\PROJECTS\models\vosk-model-en-us-0.22"
if not os.path.exists(VOSK_MODEL_PATH):
    raise FileNotFoundError(f"Vosk model not found at {VOSK_MODEL_PATH}")

vosk_model = Model(VOSK_MODEL_PATH)

# ---- Audio Queue for STT ----
q = queue.Queue()

def _callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen():
    """Offline STT using Vosk."""
    recognizer = KaldiRecognizer(vosk_model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=_callback):
        print("Listening (offline)... Speak now.")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                return result.get("text", "").strip()

# ---- TTS ----
def speak(text: str):
    """Speak text in background thread (non-blocking)."""
    def _run():
        try:
            engine = pyttsx3.init(driverName="sapi5")  # Windows driver
            engine.setProperty("rate", 175)
            engine.setProperty("volume", 1.0)
            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"[TTS ERROR] {e}")

    threading.Thread(target=_run, daemon=True).start()
