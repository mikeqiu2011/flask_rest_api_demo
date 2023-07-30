from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel, ItemTagModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint('tags', __name__, description='Operations on Tags')


@blp.route('/store/<int:store_id>/tag')
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        # if TagModel.query.filter(TagModel.store_id == store_id,
        #                          TagModel.name == tag_data['name']).first():
        #     abort(400, message='tag with the name already exist in the store')

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@blp.route('/tag/<int:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        return tag

    @blp.response(202,
                  description='deleted a tag is no item is tagged as that one',
                  examples={'message': 'Tag deleted'})
    @blp.alt_response(404,
                      description='Tag not found')
    @blp.alt_response(400,
                      description='if the tag is assigned to one or more items, '
                                  'the tag is not deleted')
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if tag.items:
            abort(400, 'tag associated with items, cannot delete')

        try:
            db.session.delete(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, str(e))

        return {'message': 'tag deleted'}


@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, str(e))

        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, str(e))

        return {
            'message': 'item removed from tag',
            'item': item,
            'tag': tag
        }
