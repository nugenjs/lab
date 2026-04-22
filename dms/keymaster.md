#

install latest wireless drivers


## Instructions
``` shell
# When image is newly installed, there is very little allocated disk space
df -h # See human readable disk space allocated

# Configure to use entire disk space
sudo raspi-config
# Advanced Options > Expand Filesystem
# Finish then reboot

sudo apt update
sudo apt install vim


echo "<you api key here>" > /home/keymaster/.es_apikey
# Lock so only current user can open
chmod 600 /home/keymaster/.es_apikey
# run filebeat script in the background
chmod filebeat.sh
filebeat.sh &

# to stop the script use
pkill -f btest.sh


# Alternatively FileBeat
## source: https://www.gunnarleffler.com/posts/raspberry_pi_filebeats/
# Install git and golang
sudo apt install git golang
# clone https://github.com/elastic/beats.git
git clone https://github.com/elastic/beats.git
$VERSION=7.15.2
```



## interlock test bet 1 2 and 3
url: interlock-test-{0}.dms.local   (1, 2, 3)
u: keymaster
p: dmsDMS

## SSH tools
putty\
winSCP\
