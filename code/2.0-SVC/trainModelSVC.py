from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import normalize
import pickle
from sklearn import svm
import json

FILENAME = 'svcModel.pk'

raw_file = open('data/dati.json')
data = json.load(raw_file)
people_pieces = data['pieces']
l = data['n_pers']
names = data['names']

v = DictVectorizer(sparse=False, sort=False)
X = v.fit_transform(people_pieces) #hot-encoding
X = normalize(X)                  #metto i vettori con norma = 1
y = [0,1,2,3]

clf = svm.SVC(gamma='auto')


clf.fit(X,y)


pickle.dump(clf, open(FILENAME, 'wb'))




