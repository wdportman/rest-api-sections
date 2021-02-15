from flask import Flask

app = Flask(__name__)
stores = [
  {
    'name': "Will's Store",
    'items': [
      {
        'name': "Will's Cool Item",
        'price': 9.99
      }
    ]
  }
]

#GET /:
@app.route('/')
def home():
  return "Hello, ¡world!"

#GET /store:
@app.route('/store')
def get_stores():
  pass

#GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
  pass

#GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
  pass

#POST /store data: {name :}
@app.route('/store', methods=['POST'])
def create_store():
  pass

#POST /store/<name> data: {name :}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
  pass

app.run(port=5000)