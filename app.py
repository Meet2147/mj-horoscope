from flask import Flask, jsonify
from horoscope import Horoscope
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


############################################
# Index
############################################

@app.route('/', methods=['GET'])
def index_route():
	return jsonify({
		'author': 'Meet Jethwa',
		'author_url': 'http://Meet2147.github.io/',
		'base_url': 'https://mjhoroscope-api.herokuapp.com/',
		'project_name': 'Horoscope API',
		
	})


############################################
# Horoscopes
###########################################

# Todays' Horoscope
@app.route('/horoscope/today/<sunsign>', methods=['GET'])
def today_horoscope_route(sunsign):
	result = dict(Horoscope.get_todays_horoscope(sunsign))
	return jsonify(date=result['date'],
				   sunsign=result['sunsign'],
				   horoscope=result['horoscope'])


# Current Week Horoscope
@app.route('/horoscope/week/<sunsign>', methods=['GET'])
def weekly_horoscope_route(sunsign):
	result = dict(Horoscope.get_weekly_horoscope(sunsign))
	return jsonify(week=result['week'],
				   sunsign=result['sunsign'],
				   horoscope=result['horoscope'])


# Current Month Horoscope
@app.route('/horoscope/month/<sunsign>', methods=['GET'])
def monthly_horoscope_route(sunsign):
	result = dict(Horoscope.get_monthly_horoscope(sunsign))
	return jsonify(month=result['month'],
				   sunsign=result['sunsign'],
				   horoscope=result['horoscope'])


# Current Year Horoscope
@app.route('/horoscope/year/<sunsign>', methods=['GET'])
def yearly_horoscope_route(sunsign):
	result = dict(Horoscope.get_yearly_horoscope(sunsign))
	return jsonify(year=result['year'],
				   sunsign=result['sunsign'],
				   horoscope=result['horoscope'])


###########################################
# Start Flask
###########################################

if __name__ == "__main__":
	app.run()


