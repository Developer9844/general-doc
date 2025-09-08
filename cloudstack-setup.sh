sudo systemctl stop cloudstack-management
sudo systemctl stop cloudstack-agent

sudo apt-get purge -y cloudstack-management cloudstack-agent cloudstack-*
sudo apt-get autoremove -y

sudo rm -rf /etc/cloudstack/
sudo rm -rf /var/log/cloudstack/
sudo rm -rf /var/lib/cloudstack/
sudo rm -rf /tmp/*

mysql -u root -p
DROP DATABASE cloud;
DROP USER 'cloud'@'localhost';
DROP USER 'cloud'@'%';
FLUSH PRIVILEGES;
EXIT;

sudo apt-get remove --purge -y openjdk-11* 
sudo apt-get autoremove -y

sudo apt install -y openjdk-11-jdk


Moon@1207


sudo systemctl daemon-reload
sudo systemctl reset-failed


apt-get update
apt-get install -y cloudstack-management cloudstack-agent
    
sudo update-ca-certificates

cloudstack-setup-databases cloud:cloud@localhost --deploy-as=root:Pa$$w0rd -i 192.168.0.233
cloudstack-setup-management




https://github.com/AhmadRifqi86/cloudstack-install-and-configure/tree/main/cloudstack-install





sudo -i
mkdir -p /etc/apt/keyrings 
wget -O- http://packages.shapeblue.com/release.asc | gpg --dearmor | sudo tee /etc/apt/keyrings/cloudstack.gpg > /dev/null
echo deb [signed-by=/etc/apt/keyrings/cloudstack.gpg] http://packages.shapeblue.com/cloudstack/upstream/debian/4.19 / > /etc/apt/sources.list.d/cloudstack.list

server.properties
- consoleproxy.ssl.enabled=false
- secstorage.ssl.enabled=false

Global settings:

secstorage.allowed.internal.site
192.168.0.233/22

consoleproxy.disable.rpfilte
false

secstorage.encrypt.copy
false

secstorage.ssl.cert.domain
blank


consoleproxy.sslEnabled
false

ca.plugin.root.auth.strictness
false


Please open the ssvm public IP https://192.41.41.161/ in the new tab of the running browser and accept the certificate warning and try again uploading the ISO.






lscpu | grep "CPU MHz"
lscpu | grep -i "max\|speed"

host.cpu.manual.speed.mhz=2400  # Replace with your actual CPU speed





Guest CIDR      : 10.1.1.0/24
Public Traffic  : 192.168.3.10 - 3.20
Pod Reserved IPs: 192.168.3.21 - 3.30





