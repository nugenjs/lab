from playsound import playsound
import subprocess
import tempfile

# ./piper --help
# usage: ./piper [options]
# options:
#    -h        --help              show this message and exit
#    -m  FILE  --model       FILE  path to onnx model file
#    -c  FILE  --config      FILE  path to model config file (default: model path + .json)
#    -f  FILE  --output_file FILE  path to output WAV file ('-' for stdout)
#    -d  DIR   --output_dir  DIR   path to output directory (default: cwd)
#    --output_raw                  output raw audio to stdout as it becomes available
#    -s  NUM   --speaker     NUM   id of speaker (default: 0)
#    --noise_scale           NUM   generator noise (default: 0.667)
#    --length_scale          NUM   phoneme length (default: 1.0)
#    --noise_w               NUM   phoneme width noise (default: 0.8)
#    --sentence_silence      NUM   seconds of silence after each sentence (default: 0.2)
#    --espeak_data           DIR   path to espeak-ng data directory
#    --tashkeel_model        FILE  path to libtashkeel onnx model (arabic)
#    --json-input                  stdin input is lines of JSON instead of plain text
#    --use-cuda                    use CUDA execution provider
#    --debug                       print DEBUG messages to the console
#    -q       --quiet              disable logging

# def speak(text, model_path="./piper/en_US-amy-low.onnx", output_path="./audio_out/hello2.wav"):
def speak(text, model_path="./piper/en_US-amy-medium.onnx"):
# def speak(text, model_path="./piper/en_GB-southern_english_female-low.onnx"):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        output_path = tmp.name
    subprocess.run([
        "./piper/build/piper",
        # "--quiet",  # Disable logging
        "--model", model_path,
        "--espeak_data", "/opt/homebrew/share/espeak-ng-data",
        "--output_file", output_path,
        "--noise_scale", "0.667",  # Adjust noise scale, default is 0.667
        # "--length_scale", "0.4",  # Adjust length scale, default is 1.0
        "--length_scale", "0.6",  # Adjust length scale, default is 1.0
        "--noise_w", "0.8",  # Adjust noise width, default is 0.8
        "--sentence_silence", "0.4",  # Adjust silence after each sentence, default is 0.2 
    ], 
    input=text.encode("utf-8"),  # Convert text to bytes for stdin

    check=True
    )

    playsound(output_path)



def speak_with_piper(text, model_path="en_US-amy-low.onnx", output_path="/tmp/piper_output.wav"):
    # Run the Piper binary and feed it text via stdin
    proc = subprocess.run(
        ["./piper", "--model", model_path, "--output_file", output_path],
        input=text.encode("utf-8"),  # Convert text to bytes for stdin
        check=True
    )

    # Play the audio using macOS's afplay
    subprocess.run(["afplay", output_path])


speak_with_piper(''' hello ''')