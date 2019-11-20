import json, pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np

FILENAME = 'RndForestModel.pk'

#prendo i dati per il training
raw_file = open('data/dati.json')
data = json.load(raw_file)
documenti = data['words']
count = data['count']
l = data['n_pers']
names = data['names']

#prendo il vocabolario delle parole
raw_file = open('data/voc.json')
data = json.load(raw_file)
vocabolary = data['vocabolary']

#input
X = [[] for _ in range(l)]

#ad ogni parola del vocabolario, per ogni documento (persona), assegno un valore di importanza
for word in vocabolary:
	docConWord = 0
	tf = [0 for _ in range(l)]

	for i in range(l):
		doc = documenti[i]
		cc = count[i]
		if word in doc:
			docConWord += 1
			tf[i] = doc[word] / cc

	idfi = np.log(4/docConWord)
	for i in range(l):
		X[i].append(tf[i] * idfi)
	
clf = RandomForestClassifier(n_estimators=300)
clf.fit(X, names)


pickle.dump(clf, open(FILENAME, 'wb'))

