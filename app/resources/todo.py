from flask_restful import Resource, reqparse
from app.models.todo import TodoModel
from datetime import datetime

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
            return todo.json(), 200
        return {'message': 'todo not found'}, 404

    def put(self, _id):
        todo = TodoModel.find_by_id(_id)
        if todo:
            data = self.parser.parse_args()

            todo.name = data['name']
            todo.description = data['description']
            todo.completed = data['completed']

            todo.save_to_db()
            return todo.json(), 200
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
        return todo.json(), 201

class TodoList(Resource):
    def get(self):
        todos = []
        for todo in TodoModel.query.all():
            todos.append(todo.json())
        return {'todo_list': todos}, 200