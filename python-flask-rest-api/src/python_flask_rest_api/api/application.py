

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# here project.db is the name of database to be created

# initialize the app with the extension
db = SQLAlchemy(app)
app.app_context().push()
api = Api(app)
user_args = reqparse.RequestParser()
"""
or create a seperate py file with content 
from application import app, db
with app.app_context():
    db.create_all()


"""

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return f"{self.name} - {self.description}"

user_args.add_argument('name', type=str, required=True, help='name can not be blank')
user_args.add_argument('description', type=str, required=True, help='description can not be blank')


"""
Client - Server communication 
"""
# the URL ('/') is associated with the root URL. So if our site's domain was www.example.org and we want to add routing to 'www.example.org/hello', we would use '/hello'.
@app.route('/')
def home():
    return '<h1>Hello Flask REST API!<h1>'

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        output.append(drink_data)

    return {"drinks": output}

# use to qudery by id for example http://127.0.0.1:5000/drinks/1
@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name":drink.name, "description": drink.description}

# to add a new record
@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()

    return {'id': drink.id}

# to delete a record
@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()

    return {'message': f'{drink.id} deleted!'}