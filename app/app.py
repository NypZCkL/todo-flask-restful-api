from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import os

app = Flask(__name__)

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

uri = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql' + uri[uri.find(':'):] #'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app.resources.todo import Todo, createTodo, TodoList

api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/')
def home():
    return 'Todo REST Api'

api.add_resource(Todo, '/todo/<int:_id>')
api.add_resource(createTodo, '/todo')
api.add_resource(TodoList, '/todos')