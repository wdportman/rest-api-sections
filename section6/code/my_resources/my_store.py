from flask_restful import Resource
from my_models.my_store import StoreModel

class Store(Resource):
  def get(self, name):
    store = StoreModel.find_by_name(name)
    if store:
      return store.json()
    return {'message': 'Store not found'}, 404
  
  def post(self, name):
    pass

  def delete(self, name):
    pass


class StoreList(Resource):
  pass