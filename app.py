from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import threading
import requests

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///currency"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Db (db.Model):
	__tablename__ = "currency"
	id = db.Column("id",db.Integer,primary_key=True)
	time = db.Column("Time",db.DateTime,default=db.func.now())
	BTC_price = db.Column("BTC_price",db.Float)
	def __init__ (self,BTC_price):
		self.BTC_price = BTC_price

def Write_rate():
	''' Function will write current btc-usd rate into database each 10 seconds '''
	threading.Timer(10.0, Write_rate).start()	# Timer

	r = requests.get("https://api.cryptonator.com/api/ticker/btc-usd")	# Request for fresh rates
	# Write into database	
	new_ex = Db(r.json()['ticker']['price'])
	db.session.add(new_ex)
	db.session.commit()
Write_rate() # Start writing into database


@app.route("/")
def index():
	return render_template("index.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
