# HTTP to MQTT Bridge
Bridge to convert HTTP requests to MQTT messages.

## REEVALUATE
```
export PATH="$HOME/.local/bin:$PATH" # add to shell config
```


## Setup & Run

### Copy Files to Raspberry Pi
``` bash
scp * <pi username>@mqtt.io:<directory of http-mqtt-bridge>/
```

### SSH into Raspberry Pi:

Install Nginx to allow ports 1-1023 to be used without sudo:
```bash
sudo apt update && sudo apt upgrade
sudo apt install nginx -y

cp <directory of http=mqtt-bridge>/nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```


Install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh 
# restart terminal or source your shell config (e.g. source ~/.zshrc) or exec $SHELL
```

Run App
```bash
cd <directory of http=mqtt-bridge>/
uv sync

# One of the run commands
uv run app.py 
uv run uvicorn app:app --host 0.0.0.0 --port 8000
```

## Setup as a service
Change `pi3` to your pi username in `http-mqtt-bridge.service` file.

Then run:
```bash
sudo cp <directory of http-mqtt-bridge>/http-mqtt-bridge.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable http-mqtt-bridge.service
sudo systemctl start http-mqtt-bridge.service
sudo systemctl status http-mqtt-bridge.service

sudo journalctl -u http-mqtt-bridge.service -f # view logs
```