from flask.globals import session
from app.models.category_model import CategoryModel
from flask import request, Blueprint, jsonify, current_app
from http import HTTPStatus


bp_category = Blueprint('bp_category', __name__, url_prefix="/category")

@bp_category.route('/', methods=['POST'])
def create_category():
    session = current_app.db.session
    body_category = request.get_json()
    name = body_category.get('name')
    new_category = CategoryModel(name=name)
    
    session.add(new_category)
    session.commit()

    return {
        'category': {
            'id': new_category.id,
            'name': new_category.name
        }
    }, HTTPStatus.CREATED



@bp_category.route('/', methods=['GET'])
def get_category():
    session = current_app.db.session

    categories_list = [
        {
            'id': category.id,
            'name': category.name
        }
        for category in session.query(CategoryModel).all()
    ]
    
    return jsonify(categories_list), HTTPStatus.OK



@bp_category.route("/<int:id>", methods=['GET'])
def get_id_category(id):
    category = CategoryModel.query.filter_by(id =id).first()
    
    return {
        'id': category.id,
        'name': category.name
    }