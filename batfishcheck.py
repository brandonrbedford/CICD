import requests

response = requests.get("http://192.168.219.128:9996")
print(response.status_code)
