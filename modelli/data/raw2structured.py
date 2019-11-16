import json
import re


NAMES = ['emma', 'michelle', 'roger', 'tim']


people_words = []
count_words = []
set_of_words = set()


for person in NAMES:
	raw_file = open(person+'.json')
	data = json.load(raw_file)

	word_list = {}
	count = 0

	for site in data:

		#prendo la parte dell'indirizzo della pagina
		if 'ategory:' in site:
			page = site.split('ategory:')[1]
		else:
			page = site.split('.org/')[1]

		#rendo tutto minuscolo e pulisco un po'
		page = page.lower()
		page = re.sub('\(|\)|%[0-9]*|l\'|,|s$|\.', '', page)


		#prendo le parole del titolo in un ...
		for word in page.split('_'):
			if word in word_list:
				word_list[word] += data[site]
			else:
				word_list[word] = data[site]
			count += data[site]
			set_of_words.add(word)

	people_words.append(word_list)
	count_words.append(count)


#cerchiamo di eliminare le parole comuni a tutte le persone (articoli preposizioni ...)

"""
ww = 'descent'
print(str(people_words[0][ww]) + "  "+ str(people_words[1][ww])+ "  "+ str(people_words[2][ww])+"  "+ str(people_words[3][ww]) )
"""
l = len(NAMES)
for word in set_of_words:
	perc = []
	for i in range(l):
		if word in people_words[i]:
			perc.append(people_words[i][word]/count_words[i])
	if len(perc)==l:
		med = sum(perc)/l
		var = 0
		for i in range(l):
			var += (med-perc[i])**2
		var /= l
		#se trovo una parola che ha poca varianza tra le persone la elimino
		if var < 9.2e-06:
			for i in range(l):
				x = people_words[i][word]
				del people_words[i][word]
				count_words[i] -= x

myJson = {
	'n_pers':l,
	'count':{i:count_words[i] for i in range(l)},
	'words':people_words
}

with open("../clean.json", "w") as outfile:
    json.dump(myJson, outfile, indent=2)
