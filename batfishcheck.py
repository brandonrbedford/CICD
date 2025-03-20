import requests
response = requests.get("http://127.0.0.1:9996")
print(response.status_code)
