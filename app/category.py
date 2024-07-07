from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/apythonrest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(100))

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

with app.app_context():
    db.create_all()

#Schemas
class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'desc')

#Only one response
category_schema = CategorySchema()

#Many responses
categories_schema = CategorySchema(many=True)

#GET
@app.route('/category', methods=['GET'])
def get_categories():
    all_categories = Category.query.all()
    result = categories_schema.dump(all_categories)
    return jsonify(result)

#GET BY ID
@app.route('/category/<id>', methods=['GET'])
def get_category_id(id):
    category = Category.query.get(id)
    return category_schema.jsonify(category)

#POST
@app.route('/category', methods=['POST'])
def insert_category():
    data = request.get_json(force=True)
    name = request.json['name']
    desc = request.json['desc']

    new_category = Category(name, desc)
    db.session.add(new_category)
    db.session.commit()

    return category_schema.jsonify(new_category)


#PUT
@app.route('/category/<id>', methods=['PUT'])
def update_category(id):
    categoryUpdate = Category.query.get(id)
    name = request.json['name']
    desc = request.json['desc']

    categoryUpdate.name = name
    categoryUpdate.desc = desc
    db.session.commit()

    return category_schema.jsonify(categoryUpdate)


#DELETE
@app.route('/category/<id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()

    return category_schema.jsonify(category)


#Welcome message
@app.route('/',methods=['GET'])
def index():
    return jsonify({'message': 'Hello, Trigo!'}), 200

if __name__=="__main__":
    app.run(debug=True)