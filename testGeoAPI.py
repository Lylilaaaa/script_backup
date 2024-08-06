import requests

url = "https://pro-api.coingecko.com/api/v3/coins/list"

response = requests.get(url)

print(response.text)