import sys
from playsound import playsound
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import subprocess
import tempfile
import time
import os


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
            "--length_scale", "0.7",  # Adjust length scale, default is 1.0
            # "--length_scale", "0.4",  # Adjust length scale, default is 1.0
            "--noise_w", "0.7",  # Adjust noise width, default is 0.8
            "--sentence_silence", "0.4",  # Adjust silence after each sentence, default is 0.2 
        ], 
        input=text.encode("utf-8"),  # Convert text to bytes for stdin

        check=True
    )

    playsound(output_path)




WHISPER_MODEL = "./whisper.cpp/models/ggml-medium.bin"
PIPER_MODEL = "en_US-amy-low.onnx"
WHISPER_BIN = "./whisper.cpp/build/bin/whisper-cli"  # Adjust if your whisper.cpp binary has a different name
PIPER_BIN = "./piper"

def record_audio(duration=5, output_path="/tmp/recording.wav"):
    print("🎙️ Recording...")
    subprocess.run([
        "sox", "-d", output_path, "trim", "0", str(duration)
    ], check=True)
    print("✅ Recording saved to", output_path)

    # samplerate = 16000  # whisper expects 16kHz mono
    # audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    # sd.wait()
    # write(output_path, samplerate, audio)
    # print("✅ Recording saved to", output_path)

def record_until_silence(threshold=500, 
                         silence_duration=2, 
                         sample_rate=16000, 
                         output_path="/tmp/recording.wav"):
    print("🎙️ Start speaking...")

    buffer = []
    silence_start = None
    frame_duration = 0.2  # 200ms
    frame_size = int(sample_rate * frame_duration)

    # def rms(data):
    #     return np.sqrt(np.mean(np.square(data)))
    def rms(data):
        if len(data) == 0:
            return 0.0
        return np.sqrt(np.mean(np.square(data.astype(np.float32))))

    
    # # Inside your recording loop (in record_until_silence)
    # level = rms(frame)
    # bar = int(level / 100)  # Scale for display
    # bar = min(bar, 50)      # Cap the max length

    # sys.stdout.write(f"\r🔊 Volume: [{('=' * bar):<50}] {level:.2f}")
    # sys.stdout.flush()

    try:
        with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
            while True:
                frame, _ = stream.read(frame_size)
                frame = frame.flatten()
                buffer.append(frame)

                level = rms(frame)
                # 12000
                # print(f"🔊 Volume: {level} < threshold: {threshold}")
                # print(f"🔊 Volume: {level:.2f}")
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
                    # print("🔊 Sound detected. Resetting silence timer.")
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
    audio_file = "./mic_input.wav"
    # record_audio(duration=20, output_path=audio_file)
    # text = transcribe_with_whisper(audio_file)
    # print("🎤 Text to speak:", text)

    # if text:
    #     speak(text)
    # speak("Hello, this is a test of the Piper text-to-speech system using Whisper for transcription.")
    record_until_silence(threshold=500, silence_duration=2, sample_rate=16000, output_path=audio_file)
    text = transcribe_with_whisper(audio_file)
    print("🎤 Text to speak:", text)

    if text:
        speak(text)

# if __name__ == "__main__":
if __name__ == "__main__":
    main()

# speak("Hello, this is a test of the Piper text-to-speech system using Whisper for transcription.")
