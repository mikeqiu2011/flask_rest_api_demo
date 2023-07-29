import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

blp = Blueprint('items', __name__, description='Operations on items')


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message='item does not exist!')

    def delete(self, item_id):
        try:
            del items[item_id]
        except KeyError:
            abort(404, message='store does not exist!')

    def put(self, item_id):
        if item_id not in items:
            abort(400, message='item id not exist!')

        item_data = request.get_json()
        if 'name' not in item_data or 'price' not in item_data:
            abort(400,
                  message='Bad request, ensure "price", "store_id" are '
                          'included in the json payload!')

        items[item_id] |= item_data

        return items[item_id]


@blp.route('/item')
class ItemList(MethodView):
    def get(self):
        return {'items': list(items.values())}

    def post(self):
        item_data = request.get_json()
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item, 201
