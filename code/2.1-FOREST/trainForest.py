import json


raw_file = open('data/dati.json')
data = json.load(raw_file)
raw_file = open('data/words.json')
vocabolary = json.load(raw_file)


print(data)
print(vocabolary)

