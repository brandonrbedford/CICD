import requests

response = requests.get("http://127.0.0.1:80")
print(response.status_code)
