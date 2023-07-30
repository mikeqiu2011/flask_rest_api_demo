from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import StoreModel

blp = Blueprint('stores', __name__, description='Operations on stores')


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
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
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message='A store with that name already exists')
        except SQLAlchemyError:
            abort(500, message='an error occurred while inserting the item')

        return store
