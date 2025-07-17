
```
docker pull docker-image
docker run -d --name container-name docker-image

sudo vim /etc/systemd/system/container-name.service
```

```
[Unit]
Description=Name-container
After=docker.service
Requires=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker start -a container-name 
ExecStop=/usr/bin/docker stop -t 2 container-name

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload
sudo systemctl start container-name.service
sudo systemctl enable container-name.service
```



systemd service file format:-
```

[Unit]
Description=Name-container
After=
Requires=

[Service]
Restart=always
User=
Group=
WorkingDirectory=
ExecStart=/usr/bin/docker start -a container-name 
StandardOutput=syslog or null
StandardError=syslog or null
SyslogIdentifier=

[Install]
WantedBy=multi-user.target
```



```
[Unit]
Description=Langflow container
After=docker.service
Requires=docker.service

[Service]
Restart=always
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/langflow/docker_example
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
```
