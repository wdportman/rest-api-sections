from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from my_security import authenticate, identity
from my_resources.my_user import UserRegister
from my_resources.my_item import Item, ItemList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'will'
api = Api(app)

jwt = JWT(app, authenticate, identity) #JWT creates a new endpoint: /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
  from my_db import db
  db.init_app(app)
  app.run(port=5000, debug=True)