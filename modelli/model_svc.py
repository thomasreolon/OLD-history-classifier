from sklearn.feature_extraction import DictVectorizer
from numpy import savetxt
import json


raw_file = open('clean.json')
data = json.load(raw_file)

people_words = data['words']

v = DictVectorizer(sparse=False)
nump_array = v.fit_transform(people_words)


savetxt('n_array.csv', nump_array, delimiter=',')

#print(people_words)
print("before")
print(nump_array)
print("after")

