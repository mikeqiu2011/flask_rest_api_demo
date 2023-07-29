import uuid

from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)


@app.get('/store')
def get_stores():
    return {'stores': list(stores.values())}


@app.post('/store')
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return store, 201


@app.get('/store/<string:id>')
def get_store(id):
    try:
        return stores[id]
    except KeyError:
        abort(404, message='store not found')


@app.get('/item')
def get_all_items():
    return {'items': list(items.values())}


@app.post('/item')
def create_item():
    item_data = request.get_json()
    if (
            'store_id' not in item_data
            or 'name' not in item_data
            or 'price' not in item_data
    ):
        abort(400,
              message='Bad request, ensure "price", "store_id" are '
                      'included in the json payload!')

    if item_data['store_id'] not in stores:
        abort(404, message='store not found')

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201


@app.get('/item/<string:id>')
def get_item(id):
    try:
        return items[id]
    except KeyError:
        abort(404, message='item not found')


if __name__ == '__main__':
    app.run(debug=True)
