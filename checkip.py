import os
from netmiko import ConnectHandler

user = os.environ["USER"]
password = os.environ["PASSWORD"]

R1 = {
    "device_type": "cisco_ios",
    "ip": "192.168.219.131",
    "username": user,
    "password": password,
}

net_connect = ConnectHandler(**R1) xxxx
output = net_connect.send_command("show ip int brief")
print(output)
