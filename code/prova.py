from sklearn import svm
from sklearn import datasets
clf = svm.SVC(gamma='scale')
iris = datasets.load_iris()
X, y = iris.data, iris.target

X = [[0,0],[0,1],[1,0],[2,2]]
y = [0,0,1,2]

print(X)
print("-----------")
print(y)

clf.fit(X, y)
