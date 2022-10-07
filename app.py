from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import os

app = Flask(__name__)

uri = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql' + uri[uri.find(':'):] #'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Todo List API"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

ma = Marshmallow(app)
class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'completed', 'date_created')

todo_schema = TodoSchema(many=False)
todos_schema = TodoSchema(many=True)

class TodoModel(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(300), nullable = False)
    completed = db.Column(db.Boolean, nullable = False, default = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.now)

    def __init__(self, name, description, completed, date_created):
        self.name = name
        self.description = description
        self.completed = completed
        self.date_created = date_created

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_db(self):
        db.session.delete(self)
        db.session.commit()

class Todo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help='This field can not be blank!'
    )
    parser.add_argument('description',
        type=str,
        required=True,
        help='This field can not be blank!'
    )
    parser.add_argument('completed',
        type=bool,
        required=True,
        help='This field can not be blank!'
    )

    def get(self, _id):
        todo = TodoModel.find_by_id(_id)
        if todo:
            return todo_schema.dump(todo), 200
        return {'message': 'todo not found'}, 404

    def put(self, _id):
        todo = TodoModel.find_by_id(_id)
        if todo:
            data = self.parser.parse_args()

            todo.name = data['name']
            todo.description = data['description']
            todo.completed = data['completed']

            todo.save_to_db()
            return todo_schema.dump(todo), 200
        return {'message': 'todo not found'}, 404
    
    def delete(self, _id):
        todo = TodoModel.find_by_id(_id)
        if todo:
            todo.delete_db()
        return {'message': 'todo deleted'}, 200

class createTodo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help='This field can not be blank!'
    )
    parser.add_argument('description',
        type=str,
        required=True,
        help='This field can not be blank!'
    )

    def post(self):
        data = self.parser.parse_args()
        todo = TodoModel(name=data['name'], description=data['description'], completed=False, date_created=datetime.now())
        todo.save_to_db()
        return todo_schema.dump(todo), 200

class TodoList(Resource):
    def get(self):
        return {'todo_list': todos_schema.dump(TodoModel.query.all())}, 200

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return 'Todo REST Api'

api.add_resource(Todo, '/todo/<int:_id>')
api.add_resource(createTodo, '/todo')
api.add_resource(TodoList, '/todos')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)