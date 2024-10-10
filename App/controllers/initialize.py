from .user import create_user
from App.database import db
from .assignment import *
from .course import *
from .staff import *

def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_course()
    create_staff()
    assign_staff()
