# Linux

# ENV VARS
`$XDG_SESSION_TYPE`: wayland or x11 (display server/compositor) 


# systemctl commands
`systemctl` is used to manage systemd services.
Common commands:
`sudo systemctl daemon-reload`: reload service files after modification\
`sudo systemctl enable yourservice`: enable service to start on boot\
`sudo systemctl start yourservice`: start the service\
`sudo systemctl stop yourservice`: stop the service\
`sudo systemctl restart yourservice`: restart the service\
`sudo systemctl status yourservice`: check the status of the service\
`systemctl is-enabled yourservice`: check if the service is enabled

# journalctl commands
`journalctl -u yourservice`: view logs for a specific service\
`journalctl -u yourservice -f`: follow logs in real-time


