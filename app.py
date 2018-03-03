from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

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


@app.route("/")
def index():
	return render_template("index.html")


''' Ajax section '''

''' Write given rate into database '''
@app.route("/save",methods = ['GET'])
def save():
	price = request.args.get("price")
	new_ex = Db(price)
	db.session.add(new_ex)
	db.session.commit()
	return "sucess"

if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)