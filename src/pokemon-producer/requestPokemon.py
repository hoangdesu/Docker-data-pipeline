import requests

url = 'https://pokeapi.co/api/v2/pokemon/'
content = requests.get(url+'25')
json = content.json()
print(json["types"][0]["type"]["name"])