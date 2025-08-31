# Text and Speech tests

Using Piper for text-to-speed, Whisper for speed-to-text, and ollama for llm, to respond to natural language requests.

## Speech-to-Text using Whisper
`brew install ffmpeg` \
`git clone https://github.com/ggerganov/whisper.cpp` \
`cd whisper.cpp` \
`make`

### download the model and size small medium large
./models/download-ggml-model.sh medium \
ggml-tiny.bin ggml-base.bin ggml-small.bin ggml-medium.bin ggml-large-v1.bin ggml-large-v2.bin

## Text-to-Speech using Piper
`git clone https://github.com/rhasspy/piper.git`
cd piper, make, cd build

### Voices:
Follow download link from [here](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/VOICES.md) \
and download voice `model.onnx` and the corresponding json

### Examples:
```
echo 'Welcome to the world of speech synthesis!' | ./{piper-repo}/build/piper --model en_US-lessac-medium.onnx --output_file welcome.wav

./{piper-repo}/build/piper --model voices/en_US-lessac/en_US-lessac.onnx --output_file output.wav --text "Hello from Piper on Mac!" --espeak_data PIPER_ESPEAK_DATA

echo "hello my name is what my name is who my name is slim shady" | ./{piper-repo}/build/piper --model ../en_US-amy-low.onnx --output_file deleteme.wav --espeak_data "/opt/homebrew/share/espeak-ng-data"
```

### Errors:
If encounter error: `Error processing file '/usr/share/espeak-ng-data/phontab': No such file or directory.` \
`brew install espeak-ng` \
`export PIPER_ESPEAK_DATA=/opt/homebrew/share/espeak-ng-data` OR pass in as an option to Piper \



## LLM Server using Ollama.cpp
`ollama serve` to start olma \
`ollama list` to see currently running \
`ollama run mistral` # probably auto downloads it


# Run
```
ollama serve
ollama run mistral

python 05_refine_whisper_mistral_stream_piper.py
```
