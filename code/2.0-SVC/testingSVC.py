from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import normalize
import json
import importlib.util
import predictSVC


#import la funzione per pulire il sito
spec = importlib.util.spec_from_file_location("site2word", "../0_function/site2word.py")
s2w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s2w)


raw_file = open('../0_test/tests.json')
data = json.load(raw_file)

l = data['n_pers']
tests = data['test']
nomi = data['names']




clf = predictSVC.getPredictor()
v = DictVectorizer(sparse=False, sort=False)


for test in tests:
	word_list = {}     
	count = 0         

	for site in test:
		parole = s2w.alanizzaSito(site)
		for word in parole:
			count = s2w.aggiornaDati(word, word_list, count, None, test, site)


	pieces = s2w.getPieces([word_list])


	X = v.fit_transform(pieces) #hot-encoding
	X = normalize(X)

	res = clf.predict(X)

	print(res)









