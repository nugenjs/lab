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


# en_GB-semaine-medium.onnx	
# en_GB-southern_english_female-low.onnx
WHISPER_MODEL = "./whisper.cpp/models/ggml-medium.bin"
# PIPER_MODEL = "en_US-amy-low.onnx"
PIPER_MODEL = "en_GB-semaine-medium.onnx"
# PIPER_MODEL = "en_GB-southern_english_female-low.onnx"
WHISPER_BIN = "./whisper.cpp/build/bin/whisper-cli"  # Adjust if your whisper.cpp binary has a different name
PIPER_BIN = "./piper"
MISTRAL_BIN = "./mistral"  # Adjust if your Mistral binary has a different name


def query_mistral(prompt):
    start = time.time()
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False  # Set to True for streaming responses
    }
    max_tries = 3
    for attempt in range(max_tries):
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            speak(f"Mistral query failed, of attempt {attempt+1} out of {max_tries}. Error: {e}")
            print(f"⚠️ Mistral query failed (attempt {attempt+1}/{max_tries}): {e}")
            time.sleep(1)
    else:
        print("❌ Mistral query failed after maximum retries.")
        return None
    end = time.time()
    print(f"⏱️ Mistral query took {end - start:.2f} seconds")
    # response = requests.post(url, json=payload)
    data = response.json()
    return data.get("response")



# cpp example https://github.com/ggml-org/whisper.cpp/tree/master/examples/command

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
        # print(f"📄 Transcription:\n{result.strip()}")
        print(f"⏱️ Done in {end - start:.2f} seconds.")
        return result.strip()
    else:
        print("⚠️ Transcription failed.")
    

def main():
    speak("What the helly?")
    audio_file = "./mic_input.wav"
    record_until_silence(threshold=500, silence_duration=2, sample_rate=16000, output_path=audio_file)
    speak("Thinking...")
    text = transcribe_with_whisper(audio_file)
    print("🎤 Text to speak:", text)

    # Example usage
    mistral_response = query_mistral(text)
    print(mistral_response)

    # # stop the python script here 
    # # return  # Removed invalid return statement
    # sys.exit(0)

    if mistral_response:
        speak(mistral_response)
    else:
        speak("Uh oh spaghetti-o")

if __name__ == "__main__":
    main()

