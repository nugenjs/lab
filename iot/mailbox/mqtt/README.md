# MQTT
Using Mosquitto for easy setup


## Setup
Raspberry Pi 3 desktopless\
ssh <pi_name>@<ip_address>\
(if first time connecting, or modifying connection):\
ssh establish host key fingerprint into ~/.ssh/known_hosts.\

``` bash
sudo apt update && sudo apt upgrade -y
sudo apt install vim -y  # optional, but vim da goat
sudo apt install mosquitto -y
# can install mosquitto-clients if needed to test on same device

sudo systemctl enable mosquitto
# start mosquitto on boot

# Configure, and allow access beyond localhost
sudo vim /etc/mosquitto/conf.d/default.conf
\```
listener 1883
allow_anonymous true
\```
sudo systemctl restart mosquitto

# Setting up username and password for mosquitto
sudo mosquitto_passwd -c /etc/mosquitto/passwd MQTT_USER
sudo vim /etc/mosquitto/conf.d/default.conf
\```
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
\```
sudo systemctl restart mosquitto

# If installed mosquitto-clients
mosquitto_sub -h localhost -t test/topic -u MQTT_USER -P MQTT_PASS
mosquitto_pub -h localhost -t test/topic -m "hello" -u MQTT_USER -P MQTT_PASS
```



## Bus over Queue
The choice of using a bus over queue is due to:
- disregard of durability
- not needing ordering
- one to many messages




## Sources
[kafka durability and availability](https://medium.com/@msrijita189/understanding-kafka-durability-and-availability-a832c5535678)