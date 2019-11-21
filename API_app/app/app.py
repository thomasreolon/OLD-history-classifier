from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api
import svc, forest

app = Flask(__name__)
api = Api(app)


clfSVC = svc.getPredictor()
clfForest = forest.getPredictor()

def parseInput():
	body = request.get_json(force=True,silent=True)
	if body == None:
		req = str((request.data))
		if 'text=' in req:
			st = req.split('text=')[1]
			if len(st) > 2:
				body = svc.stringToDict(st)
	return body



#homepage
class Home(Resource):
	def get(self):
		return current_app.send_static_file('home.html')
	def post(self):
		return current_app.send_static_file('home.html')

#homepage
class ApiDoc(Resource):
	def get(self):
		return current_app.send_static_file('doc.html')
	def post(self):
		return current_app.send_static_file('doc.html')

#api page svc 
class SVCPage(Resource):
	def get(self):
		return "use post method, attaching a JSON with the list of wiki web pages"
	def post(self):
		body = parseInput()

		if body != None:
			X = clfSVC.formatInput(body)
			r = clfSVC.predict(X)
			res = jsonify("{'name':'"+r+"'}")
		else:
			res = jsonify("{'message':'errore nel parsing dei dati'}")
		return res

#api page random forest
class ForestPage(Resource):
	def get(self):
		return "use post method, attaching a JSON with the list of wiki web pages"
	def post(self):
		body = parseInput()

		if body != None:
			X = clfForest.formatInput(body)
			r = clfForest.predict(X)
			res = jsonify("{'name':'"+r+"'}")
		else:
			res = jsonify("{'message':'errore nel parsing dei dati'}")
		return res





api.add_resource(Home, '/')
api.add_resource(ApiDoc, '/api')
api.add_resource(SVCPage, '/api/svc')
api.add_resource(ForestPage, '/api/forest')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')


