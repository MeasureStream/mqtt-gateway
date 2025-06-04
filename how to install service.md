```
sudo nano /etc/systemd/system/mqtt-gateway.service
```

and inserted the content of ./mqtt-gateway.service

```
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

```

To start the service at the boot 

```
sudo systemctl enable mqtt-gateway.service
sudo systemctl start mqtt-gateway.service

```
