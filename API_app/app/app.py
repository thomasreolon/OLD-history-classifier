from flask import Flask
from flask_restful import Resource, Api
import svc, fs

app = Flask(__name__)
api = Api(app)

with open('pages/home.html', 'r') as content_file:
	homeHtml = content_file.read()

clf = svc.getPredictor()

#homepage
class Home(Resource):
	def get(self):
		return homeHtml
	def post(self):
		return homeHtml


#api page
class ApiPage:
	def get(self):
		return "use post method, attaching a JSON with the list of wiki web pages"
	def post(self):
		body = request.get_json(force=True,silent=True)
		if body == None:
			res = 'unable to parse JSON'
		else:
			X = clf.formatInput(body)
			r = clf.predict(X)
			res = 'secondo me è stato cercato da: ' + r
		return res





api.add_resource(Home, '/')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')