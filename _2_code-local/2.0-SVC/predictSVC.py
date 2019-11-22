import pickle

FILENAME = 'svcModel.pk'



class svcPredictor:
	def __init__(self):
		self.clf = pickle.load(open(FILENAME, 'rb'))

	def predict(self,arr):
		return self.clf.predict(arr)


def getPredictor():
	return svcPredictor()





