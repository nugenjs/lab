import threading
import queue
import tempfile
import subprocess
from dataclasses import dataclass
from playsound import playsound

# WORK IN PROGRESS

# === Config ===
PIPER_BIN = "./piper/build/piper"
ESPEAK_DATA = "/opt/homebrew/share/espeak-ng-data"
PIPER_MODEL_DIR = "./piper"  # Directory containing .onnx models

# === Dataclass for TTS Jobs ===
@dataclass
class SpeechTask:
    text: str
    model: str
    length_scale: float = 1.0

# === TTS Engine using Piper ===
def speak_with_piper(task: SpeechTask):
    model_path = f"{PIPER_MODEL_DIR}/{task.model}"
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        output_path = tmp.name

    cmd = [
        PIPER_BIN,
        "--quiet",
        "--model", model_path,
        "--espeak_data", ESPEAK_DATA,
        "--output_file", output_path,
        "--noise_scale", "0.667",
        "--length_scale", str(task.length_scale),
        "--noise_w", "0.7",
        "--sentence_silence", "0.4"
    ]

    print(f"[TTS] Synthesizing: '{task.text}' with model '{task.model}' and length_scale {task.length_scale}")
    subprocess.run(cmd, input=task.text.encode("utf-8"), check=True)
    playsound(output_path)

# === Speech Manager ===
class SpeechManager:
    def __init__(self, default_model="en_US-amy-medium.onnx", default_length_scale=0.6):
        self.queue = queue.Queue()
        self.default_model = default_model
        self.default_length_scale = default_length_scale
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def speak(self, text: str, model: str = None, length_scale: float = None):
        task = SpeechTask(
            text=text,
            model=model or self.default_model,
            length_scale=length_scale or self.default_length_scale
        )
        print(f"[TTS] Queueing: {task}")
        self.queue.put(task)

    def _worker(self):
        while True:
            task = self.queue.get()
            if task is None:
                print("[TTS] Stopping speech thread.")
                break
            speak_with_piper(task)
            self.queue.task_done()

    def stop(self):
        self.queue.put(None)
        self.thread.join()



if __name__ == "__main__":
    speech = SpeechManager(
        default_model="en_GB-semaine-medium.onnx",
        default_length_scale=0.6
    )

    try:
        speech.speak(
            "What the helly",
            model="en_GB-southern_english_female-low.onnx",
            length_scale=0.3
        )
        speech.queue.join()  # Wait for all tasks to finish
    finally:
        speech.stop()
