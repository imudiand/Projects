from web import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Harshit'}  # fake user
	reviews = [  # fake array of reviews
		{ 
			'author': {'nickname': 'John'}, 
			'body': 'Beautiful ambience & great tasting coffee' 
		},
		{ 
			'author': {'nickname': 'Susan'}, 
			'body': 'Top class customer service !' 
		}
	]
	return render_template('index.html', title="Imudianda Coffeeshop", user=user, reviews=reviews)