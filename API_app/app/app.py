from flask import Flask, current_app, request, jsonify
from flask_restful import Resource, Api
import svc

app = Flask(__name__)
api = Api(app)


clf = svc.getPredictor()

#homepage
class Home(Resource):
	def get(self):
		return current_app.send_static_file('home.html')
	def post(self):
		return current_app.send_static_file('home.html')


#api page
class ApiPage(Resource):
	def get(self):
		return "use post method, attaching a JSON with the list of wiki web pages"
	def post(self):
		body = request.get_json(force=True,silent=True)

		if body == None:
			req = str((request.data))
			if 'text=' in req:
				st = req.split('text=')[1]
				if len(st) > 2:
					body = svc.stringToDict(st)

		if body != None:
			X = clf.formatInput(body)
			r = clf.predict(X)
			res = jsonify("{'name':'"+r+"'}")
		else:
			res = jsonify("{'message':'errore nel parsing dei dati'}")
		
		return res





api.add_resource(Home, '/')
api.add_resource(ApiPage, '/api/svc')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')


