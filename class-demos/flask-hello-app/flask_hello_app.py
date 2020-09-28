from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres@localhost:5432/person"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Person(db.Model):
	__tablename__ = 'persons'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())

	def __repr__(self):
		return self.name

db.create_all()

@app.route("/")
def index():
	person = Person.query.first()
	return f"Hello, {person}"

if __name__ == '__main__':
	app.run(debug=True)