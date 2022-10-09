from ..app import db
from datetime import date, datetime
from json import dumps

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

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
    
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'completed': self.completed,
            'date_created': dumps(self.date_created, indent=4, sort_keys=True, default=json_serial)
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_db(self):
        db.session.delete(self)
        db.session.commit()