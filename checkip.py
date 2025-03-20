import os
from netmiko import ConnectHandler

USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]

r1 = {
    "device_type": "cisco_ios",
    "ip": "192.168.219.131",
    "username": USER,
    "password": PASSWORD,
}

net_connect = ConnectHandler(**r1)
output = net_connect.send_command("show ip int brief")
print(output)