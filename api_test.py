import requests

response = requests.get('https://www.bankofcanada.ca/valet/lists/groups/json')
data = response.json()
print(data)
