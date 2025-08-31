import sys
from playsound import playsound
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import subprocess
import tempfile
import time
import os
import requests
import json
import re
import threading
import queue



# en_GB-semaine-medium.onnx	
# en_GB-southern_english_female-low.onnx
WHISPER_MODEL = "./whisper.cpp/models/ggml-medium.bin"
# PIPER_MODEL = "en_US-amy-low.onnx"
PIPER_MODEL = "en_GB-semaine-medium.onnx"
# PIPER_MODEL = "en_GB-southern_english_female-low.onnx"
WHISPER_BIN = "./whisper.cpp/build/bin/whisper-cli"  # Adjust if your whisper.cpp binary has a different name
PIPER_BIN = "./piper"
MISTRAL_BIN = "./mistral"  # Adjust if your Mistral binary has a different name


# en_GB-semaine-medium.onnx	
# en_GB-southern_english_female-low.onnx
def speak(text, model_path="./piper/en_US-amy-medium.onnx"):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        output_path = tmp.name
    subprocess.run([
            "./piper/build/piper",
            "--quiet",  # Disable logging
            "--model", model_path,
            "--espeak_data", "/opt/homebrew/share/espeak-ng-data",
            "--output_file", output_path,
            "--noise_scale", "0.667",  # Adjust noise scale, default is 0.667
            "--length_scale", "0.6",  # Adjust length scale, default is 1.0
            # "--length_scale", "0.4",  # Adjust length scale, default is 1.0
            "--noise_w", "0.7",  # Adjust noise width, default is 0.8
            "--sentence_silence", "0.4",  # Adjust silence after each sentence, default is 0.2 
        ], 
        input=text.encode("utf-8"),  # Convert text to bytes for stdin

        check=True
    )

    playsound(output_path)



# === Speech Queue Manager ===
class SpeechManager:
    def __init__(self):
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def speak(self, text):
        self.queue.put(text)
        # speak(text, model_path=PIPER_MODEL)
        # speak(text)

    def _worker(self):
        while True:
            text = self.queue.get()
            if text is None:
                break
            self._speak_with_piper(text)
            self.queue.task_done()

    def _speak_with_piper(self, text):
        # print(f"[TTS] Speaking: {text}")
        # subprocess.run(["piper", "--text", text, "--voice", "en_US-lessac"], check=True)
        speak(text)

    def stop(self):
        self.queue.put(None)
        self.thread.join()


# === Streaming + Sentence Detection ===
def stream_mistral_and_speak(prompt, speech_manager):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": True
    }

    buffer = ""
    sentence_end_pattern = re.compile(r'([.!?])(?=\s|$)')

    with requests.post(url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if not line:
                continue
            data_str = line.decode('utf-8')
            # if not chunk.startswith("data:"):
            #     continue
            # chunk_text = chunk[5:].strip()
            # if chunk_text == "[DONE]":
            #     break

            try:
                data = json.loads(data_str)
                token = data.get("response", "")
                buffer += token
                done = data.get("done", False)

                print(f"[Mistral] Received chunk: {token}")

                # Process complete sentences
                while True:
                    match = sentence_end_pattern.search(buffer)
                    if not match:
                        break
                    end = match.end()
                    sentence = buffer[:end].strip()
                    buffer = buffer[end:].lstrip()
                    speech_manager.speak(sentence)

                print(f"[Mistral] Buffer: {buffer}")
                if done:
                    if buffer.strip():
                        speech_manager.speak(buffer.strip())
                    buffer = ""  # Clear buffer after processing
                    

            except json.JSONDecodeError:
                continue

    # Speak any remaining buffer
    if buffer.strip():
        speech_manager.speak(buffer.strip())



# === Usage Example ===
if __name__ == "__main__":
    speech = SpeechManager()
    try:
        user_prompt = "Tell me a story about a brave little toaster who saves the world, but in one paragraph."
        stream_mistral_and_speak(user_prompt, speech)
        speech.queue.join()  # Wait for all speech to finish
    finally:
        speech.stop()




# def speak_async(text):
#     threading.Thread(target=speak, args=(text,), daemon=True).start()



# def mistral_stream(prompt):
#     start = time.time()
#     url = "http://localhost:11434/api/generate"
#     payload = {
#         "model": "mistral",
#         "prompt": prompt,
#         "stream": True  # Enable streaming responses
#     }
#     try:
#         response = requests.post(url, json=payload, stream=True, timeout=10)
#         response.raise_for_status()
#         for line in response.iter_lines():
#             if line:
#                 data = line.decode('utf-8')
                
#                 print(data)  # Process the streamed data as needed
#     except requests.RequestException as e:
#         speak(f"Mistral streaming failed. Error: {e}")
#         print(f"⚠️ Mistral streaming failed: {e}")
#     end = time.time()
#     print(f"⏱️ Mistral streaming took {end - start:.2f} seconds")




# def main():
#     # Example usage
#     mistral_response = query_mistral('what are you')
#     mistral_stream1 = mistral_stream('what are you')
#     print(mistral_stream1)

#     # # stop the python script here 
#     # # return  # Removed invalid return statement
#     # sys.exit(0)

#     # if mistral_response:
#     #     speak(mistral_response)
#     # else:
#     #     speak("try again idiot")

# # if __name__ == "__main__":
# if __name__ == "__main__":
#     main()

