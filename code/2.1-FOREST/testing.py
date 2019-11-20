from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import normalize
import json, pickle
import importlib.util

#import la funzione per pulire il sito
spec = importlib.util.spec_from_file_location("site2word", "../0_function/site2word.py")
s2w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s2w)

#prendo i siti per il testing
raw_file = open('../0_test/tests.json')
data = json.load(raw_file)
l = data['n_pers']
tests = data['test']
nomi = data['names']

#prendo il vocabolario
raw_file = open('data/voc.json')
vocabolary = (json.load(raw_file))['vocabolary']

#carico il modello
clf = pickle.load(open('RndForestModel.pk', 'rb'))


for i in range(l):
	test = tests[i]
	word_list = {}     
	count = 0         

	for site in test:
		parole = s2w.alanizzaSito(site)
		for word in parole:
			count = s2w.aggiornaDati(word, word_list, count, None, test, site)

	# calcolo la % con cui compare ogni parola
	X = []

	for word in vocabolary:
		tf = 0
		if word in word_list:
			tf = word_list[word] / count
		X.append(tf)

	#stampo la predizione del modello
	print(clf.predict([X]))



