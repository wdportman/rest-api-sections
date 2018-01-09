from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT
from flask_uploads import configure_uploads, patch_request_class, IMAGES

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.image import Image,ImageServer,image_set

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

app.config['UPLOADED_IMAGES_DEST'] = 'static/img'
patch_request_class(app,10 * 1024 * 1024)   # restrict max upload image size to 10MB
configure_uploads(app,image_set)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Image, '/image/upload')
api.add_resource(ImageServer, '/image')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
