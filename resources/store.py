import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint('stores', __name__, description='Operations on stores')


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message='store does not exist!')

    def delete(self, store_id):
        try:
            del stores[store_id]
        except KeyError:
            abort(404, message='store does not exist!')


@blp.route('/store')
class StoreList(MethodView):
    def get(self):
        return {'stores': list(stores.values())}

    def post(self):
        store_data = request.get_json()
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store, 201
