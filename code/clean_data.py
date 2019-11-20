import json, random, numpy
import importlib.util


#import la funzione per pulire il sito
spec = importlib.util.spec_from_file_location("site2word", "0_function/site2word.py")
s2w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s2w)


#costanti
SRCFOLDER = '../raw/'
NAMES = ['emma', 'michelle', 'roger', 'tim']


people_words = []		#contiene ogni word_list
count_words = []		#contiene ogni count
set_of_words = set()	#tutte le parole che sono state trovate
people_test = []		#

for person in NAMES:
	raw_file = open(SRCFOLDER+person+'.json')
	data = json.load(raw_file)

	word_list = {}     # parola -> quante volte è comparsa in tutta la cronologia
	count = 0          # totale delle parole comparse
	test = {}          # alcune url vengono usate per il testing

	##
	# per ogni sito nel json decido se: pulirlo e metterlo nel training set, metterlo nel validation set
	##
	for site in data:

		if random.randint(0, 100) > 10: #training set	
			parole = s2w.alanizzaSito(site)
			for word in parole:
				count = s2w.aggiornaDati(word, word_list, count, set_of_words, data, site)

		else:#validation set
			test[site] = data[site]

	people_words.append(word_list)
	count_words.append(count)
	people_test.append(test)



#cerchiamo di eliminare le parole comuni a tutte le persone (articoli preposizioni ...)
l = len(NAMES)
toDel = set()
for word in set_of_words:
	perc = []
	for i in range(l):
		if word in people_words[i]:
			perc.append(people_words[i][word]/count_words[i])

	#se tutti usano questa parola, controllo se la usano con la stessa percentuale
	if len(perc)==l:
		med = sum(perc)/l
		var = 0
		for i in range(l):
			var += (med-perc[i])**2
		var /= l
		#se trovo una parola che ha poca varianza tra tutti la elimino
		if var < 9.2e-06: #trovato ad occhio
			for i in range(l):
				x = people_words[i][word]
				del people_words[i][word]
				count_words[i] -= x
			toDel.add(word)
set_of_words = set_of_words.difference(toDel)


# dati per il random forest ???
treeJson = {
	'n_pers':l,
	'words':people_words,
	'count':count_words,
	'names':NAMES
}
with open("2.1-FOREST/data/dati.json", "w") as outfile:
    json.dump(treeJson, outfile, indent=2)

#vocabolario
idf = {}
for word in set_of_words:
	tot = 0
	for i in range(l):
		if word in people_words[i]:
			tot+=1
	idf[word] = tot

topWords = set()
for i in range(l):
	top = []
	for word in people_words[i]:
		tdIdf = numpy.log(l/idf[word]) * people_words[i][word]/count 
		top.append((word,tdIdf))

	mostFrequent = sorted(top, key=lambda tup: tup[1])
	for word,_ in mostFrequent[-200:]:
		topWords.add(word)


voc = [word for word in topWords]
list.sort(voc)
print(voc)

vocab = {
	'vocabolary':voc,
}
with open("2.1-FOREST/data/voc.json", "w") as outfile:
    json.dump(vocab, outfile, indent=2)



# test
testJson = {
	'n_pers':l,
	'test':people_test,
	'names':NAMES
}

with open("0_test/tests.json", "w") as outfile:
    json.dump(testJson, outfile, indent=2)


#dati per l'SVC
people_pieces = s2w.getPieces(people_words)


svcJson = {
	'n_pers':l,
	'pieces':people_pieces,
	'names':NAMES
}

with open("2.0-SVC/data/dati.json", "w") as outfile:
    json.dump(svcJson, outfile, indent=2)