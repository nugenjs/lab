# Baby Llama
Lightweight LLM(s) ran on Ollama.cpp on Raspberry Pi 5 4GB.


## Steps used to set up
1. Raspberry Pi OS Lite (64-bit) OS on SD card using Raspberry Pi Imager
2. SSH into Pi: `ssh pi@<ip address>`
3. Update and upgrade OS: `sudo apt update && sudo apt upgrade -y`
4. Install vim: `sudo apt install vim -y`  # optional, but vim da goat
5. Install Ollama: Try option 1 below. If it fails, try option 2.
    1. Use Curl:
    - `curl -fsSL https://ollama.com/install.sh | sh`
    2. Use Aria2:
    - `sudo apt install aria2 -y`
    - `aria2c -x 8 -s 8 -k 1M --max-tries=10 --retry-wait=2 "https://github.com/ollama/ollama/releases/download/v0.11.4/ollama-linux-amd64.tgz" -d /tmp/`
    - `sudo tar -xvzf /tmp/ollama-linux-amd64.tgz -C /usr/local/bin/`
    - If needed to save space: `sudo rm /tmp/ollama-linux-amd64.tgz`
6. `ollama version`  # should show version if installed correctly
7. May need to run `ollama serve` if not already running
8. In another terminal, SSH into Pi again and run model: `ollama run <choose a model | llama3.2>`
9. Optional: Create alias for ollama command. Add to `~/.bashrc` or `~/.zshrc`:
    - `alias ollama='/usr/local/bin/ollama'`
    - `source ~/.bashrc` or `source ~/.zshrc`



## Test Results
`State without running Ollama.cpp` free -h
               total        used        free      shared  buff/cache   available
Mem:           3.9Gi       205Mi       2.6Gi       3.9Mi       1.2Gi       3.7Gi
Swap:          511Mi       8.0Mi       503Mi
`llama3.2`  free -h
               total        used        free      shared  buff/cache   available
Mem:           3.9Gi       2.8Gi        54Mi       3.9Mi       1.2Gi       1.2Gi
Swap:          511Mi       8.0Mi       503Mi


## Sources
- [How to run a Large Language Model (LLM) on a Raspberry Pi 4 ](https://www.reddit.com/r/raspberry_pi/comments/1ati2ki/how_to_run_a_large_language_model_llm_on_a/)
- [Ollama failing to download with curl](https://dev.to/bruceowenga/when-curl-fails-you-why-aria2-is-your-download-hero-n36)