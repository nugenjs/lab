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




PIPER_MODEL_SOUF_ENGLISH_LOW = "en_GB-southern_english_female-low.onnx"
PIPER_MODEL_AMY_MED = "en_US-amy-medium.onnx"
PIPER_MODEL_AMY_LOW = "en_US-amy-low.onnx"
PIPER_MODEL_SEMAINE_MED = "en_GB-semaine-medium.onnx"
WHISPER_MODEL = "./whisper.cpp/models/ggml-medium.bin"
# PIPER_MODEL = "en_GB-southern_english_female-low.onnx"
WHISPER_BIN = "./whisper.cpp/build/bin/whisper-cli"  # Adjust if your whisper.cpp binary has a different name
PIPER_BIN = "./piper"
MISTRAL_BIN = "./mistral"  # Adjust if your Mistral binary has a different name







# last_checkpoint_time = time.time()

# def time_since_last_checkpoint():
#     global last_checkpoint_time
#     current_time = time.time()
#     elapsed = current_time - last_checkpoint_time
#     last_checkpoint_time = current_time
#     print(f"⏱️ Time since last checkpoint: {elapsed:.2f} seconds")









# cpp example https://github.com/ggml-org/whisper.cpp/tree/master/examples/command

# en_US-amy-medium.onnx
# en_GB-semaine-medium.onnx	
# en_GB-southern_english_female-low.onnx
def speak(text, model="en_US-amy-medium.onnx", length_scale=0.6):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        output_path = tmp.name
    model_path = f"./piper/{model}"
    subprocess.run([
            "./piper/build/piper",
            "--quiet",  # Disable logging
            "--model", f"{model_path}",
            "--espeak_data", "/opt/homebrew/share/espeak-ng-data",
            "--output_file", output_path,
            "--noise_scale", "0.667",  # Adjust noise scale, default is 0.667
            "--length_scale", f"{length_scale}",  # Adjust length scale, default is 1.0
            # "--length_scale", "0.4",  # Adjust length scale, default is 1.0
            "--noise_w", "0.7",  # Adjust noise width, default is 0.8
            "--sentence_silence", "0.4",  # Adjust silence after each sentence, default is 0.2 
        ], 
        input=text.encode("utf-8"),  # Convert text to bytes for stdin

        check=True
    )

    playsound(output_path)





def record_until_silence(threshold=500, 
                         silence_duration=2, 
                         sample_rate=16000, 
                         output_path="/tmp/recording.wav"):
    print("🎙️ Start speaking...")

    buffer = []
    silence_start = None
    frame_duration = 0.2  # 200ms
    frame_size = int(sample_rate * frame_duration)

    def rms(data):
        if len(data) == 0:
            return 0.0
        return np.sqrt(np.mean(np.square(data.astype(np.float32))))

    try:
        with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
            while True:
                frame, _ = stream.read(frame_size)
                frame = frame.flatten()
                buffer.append(frame)

                level = rms(frame)
                bar = int(level / 100)  # Scale for display
                bar = min(bar, 50)      # Cap the max length

                sys.stdout.write(f"\r🔊 Volume: [{('=' * bar):<50}] {level:.2f}")
                sys.stdout.flush()

                if level < threshold:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > silence_duration:
                        print("🛑 Silence detected. Stopping...")
                        break
                else:
                    silence_start = None
    except KeyboardInterrupt:
        print("Recording interrupted.")

    # Concatenate all frames and write to file
    audio = np.concatenate(buffer)
    write(output_path, sample_rate, audio)
    print(f"✅ Audio saved to {output_path}")
    return output_path


def transcribe_with_whisper(audio_path):
    # === TRANSCRIBE ===
    cmd = [
        WHISPER_BIN,
        "-m", WHISPER_MODEL,
        "-f", audio_path,
        "-l", "en",
        "--no-prints",
        "-otxt"
    ]
    start = time.time()
    subprocess.run(cmd)
    end = time.time()


    # === READ TRANSCRIPT ===
    txt_output = audio_path + ".txt"
    if os.path.exists(txt_output):
        with open(txt_output, "r") as f:
            result = f.read()
        print(f"⏱️ Done in {end - start:.2f} seconds.")
        return result.strip()
    else:
        print("⚠️ Transcription failed.")




# === Speech Queue Manager ===
class SpeechManager:
    def __init__(self, default_model=None, default_length_scale=1.0):
        self.queue = queue.Queue()
        self.default_model = default_model
        self.default_length_scale = 0.6
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def speak(self, text, model=None, length_scale=None):
        self.queue.put({
            "text": text, 
            "model": model or self.default_model, 
            "length_scale": length_scale or self.default_length_scale
        })

    def _worker(self):
        print("[TTS] Worker started.")
        while True:
            item = self.queue.get()
            if item is None:
                break
            self._speak_with_piper(item["text"], item["model"], item["length_scale"])
            self.queue.task_done()

    def _speak_with_piper(self, text, model, length_scale):
        speak(text, model, length_scale)


    def stop(self):
        self.queue.put(None)
        self.thread.join()


# === Streaming + Sentence Detection ===
def stream_mistral_and_speak(prompt, speech_manager):
    full_response = ""
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


                # Process complete sentences
                while True:
                    match = sentence_end_pattern.search(buffer)
                    if not match:
                        break
                    end = match.end()
                    sentence = buffer[:end].strip()
                    buffer = buffer[end:].lstrip()
                    full_response += sentence + " "
                    
                    speech_manager.speak(sentence)

                if done:
                    if buffer.strip():
                        full_response += buffer.strip() + " "
                        speech_manager.speak(buffer.strip())
                    buffer = ""  # Clear buffer after processing
                    

            except json.JSONDecodeError:
                continue

    # Speak any remaining buffer
    if buffer.strip():
        full_response += buffer.strip() + " "
        speech_manager.speak(buffer.strip())

    return full_response




    

def main():
    speech = SpeechManager(
        default_model=PIPER_MODEL_AMY_MED,
        default_length_scale=0.3
        # default_model="en_GB-semaine-medium.onnx",
        # default_length_scale=0.6
    )


    while True:
        chat_history = ""
        chat_history_file = open("chat_history.txt", "a+")
        chat_history_file.seek(0)
        chat_history = chat_history_file.read()
        print("Chat history loaded:")
        print(chat_history)

        # speak("Hey esé. Welcome to 7-Eleven holmes", model=PIPER_MODEL_SOUF_ENGLISH_LOW, length_scale=0.45)
        piper_file_output = "./mic_input.wav"
        record_until_silence(threshold=500, silence_duration=2, sample_rate=16000, output_path=piper_file_output)
        # speak("alright then, hold up mate, let me think about it, you ignorant piece of shit")
        # speech.speak("What the hell",
        #                  model='en_GB-southern_english_female-low.onnx', length_scale=0.3)

        # print("got here 1")
        # speech.speak("Give me a minute foo",
        #                  model='en_GB-semaine-medium.onnx', length_scale=0.45)
        # print("got here 2")
        user_prompt = transcribe_with_whisper(piper_file_output)
        print("got here 3")

        # if user_prompt is empty
        if user_prompt.strip() == "" or user_prompt == '[silence]':
            print("⚠️ No speech detected.")
            break
        if re.search(r'\[[A-Z,a-z,_]*\]', user_prompt):
            print("⚠️ Silent audio detected.")
            break

        try:
            # user_prompt = "Tell me a story about a brave little toaster who saves the world, but in one paragraph."
            # full_response = stream_mistral_and_speak(f"User: {user_prompt}", speech)
            full_response = stream_mistral_and_speak(f'''{chat_history}
    User: {user_prompt}''', speech)
            print("got here 4")
            print(f"🎤 Mistral response: {full_response.strip()}")
            speech.queue.join()  # Wait for all speech to finish
        except Exception as e:
            print(f"⚠️ Error occurred: {e}")
        # finally:
        #     speech.stop()

        # write user_prompt to a file
        # with open("chat_history.txt", "w+") as f:
        #     f.write(f"User: {user_prompt}\n")
        #     f.write(f"Mistral: {full_response.strip()}\n")
        chat_history_file.write(f"User: {user_prompt}\n")
        chat_history_file.write(f"{full_response.strip()}\n")
        chat_history_file.close()


    speech.stop()

    # Example usage
    # mistral_response = query_mistral(text)
    # print(mistral_response)

    # # stop the python script here 
    # # return  # Removed invalid return statement
    # sys.exit(0)

    # if mistral_response:
    #     speak(mistral_response)
    # else:
    #     speak("How about you actually run the llm, you lazy bastard?")

# if __name__ == "__main__":
if __name__ == "__main__":
    main()

