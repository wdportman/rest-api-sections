from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from my_security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'will'
api = Api(app)

jwt = JWT(app, authenticate, identity) #JWT creates a new endpoint: /auth

items = []

class Item(Resource):
  @jwt_required()
  def get(self, name):
    item = next(filter(lambda x: x['name'] == name, items), None)
    return {'item': item}, 200 if item else 404
  
  def post(self, name):
    if next(filter(lambda x: x['name'] == name, items), None) is not None:
      return {'message': "An item with name '{}' already exists.".format(name)}, 400
    data = request.get_json()
    item = {'name': name, 'price': data['price']}
    items.append(item)
    return item, 201

  def delete(self, name):
    global items
    items = list(filter(lambda x: x['name'] != name, items))
    return {'message': 'Item deleted'}



class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)