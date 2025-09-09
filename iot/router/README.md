# Router
OpenWRT, specifically GL.iNet's Flint 2\
For now, IOT devices and message

## Setup
### Create separate network for IOT and don't allow IOT to access LAN:\
Guest Wifi over 2.4ghz\
OpenWRT/Luci/Network/Firewall\
Add new zone "iotZone"\
"iotZone" => reject: {input: reject, output: accept, forward: reject}\
Give "lan" ability to forward to "iotZone".

### Static IP for devices:\
OpenWRT/Luci/Status/Overview\
Active DHCP Leases\
Set Static: e.g. {Hostname: "mqtt", "IP address": "192.168.9.216"}\
Hostname in this case is the name the device broadcasts to be registered with the router.

### Custom Hostnames:\
OpenWRT/Luci/Network/Hostnames\
Add: e.g {Hostname: "mqtt.iot", "IP address": "192.168.9.216"}

### Force DNS through router
Skip if "Custom Hostnames" works as-is\
Add firewall redirect so clients can't bypass dnsmasq\
OpenWRT/Luci/Network/Firewall/Port Forwards\
Add\
```
Name: Force-DNS
Protocol: TCP UDP
Source zone: lan
External port: 53
Destination zone: lan
Internal IP address: <router's IP|192.168.8.1>
Internal port: 53
```
Save and apply


### Provide DHCP clients DNS options
Skip if "Custom Hostnames" works as-is\
This will let clients requesting DHCP from OpenWRT know about custom DNS\
OpenWRT/Luci/Network/Interfaces\
Edit on LAN\
DHCP Server/Advanced Settings\
DHCP-Options\
6,192.168.8.1\
Save and apply


### Domain overrides incase hostnames are ignored:\
Skip if "Custom Hostnames" works as-is\
ssh into root@192.168.8.1 # OpenWRT's IP\
``` bash
# This works on normal OpenWRT, but was having issues with GL.iNet's custom firmware
uci add dhcp domain
uci set dhcp.@domain[-1].name = "mqtt.io"
uci set dhcp.@domain[-1].ip = "192.168.9.216"
uci commit dhcp
/etc/init.d/dnsmasq restart
# check if works with
cat /tmp/dnsmasq.d/*
# should have hostname as a result

# Alternatively
uci add_list dhcp.@dnsmasq[0].address="/mqtt.io/192.168.9.216"
uci commit dhcp
/etc/init.d/dnsmasq restart
```

``` bash
# This works for my router with GL.iNet's custom firmware
echo "address=/mqtt.io/192.168.9.216" >> /etc/dnsmasq.conf
/etc/init.d/dnsmasq restart
# check if works with
cat /tmp/dnsmasq.conf
# should have hostname at the end of file
```

These can then be confirmed with:\
`nslookup <mqtt.io|custom_hostname>`\
`ping <mqtt.io|custom_hostname>`\
but these might give different results based on different machines.\
Mac:
``` bash
# check dns resolvers on mac
scutil --dns | grep -A2 "resolver #1"
# flush DNS cache
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```
