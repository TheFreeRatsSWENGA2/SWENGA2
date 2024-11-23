from .user import create_user
from .student import create_student
from App.database import db
from .assignment import *
from .course import *
from .staff import *
from .admin import *
from .host import *

def initialize():
    db.drop_all()
    db.create_all()
    create_student('Kailash', 'kaipass')
    create_student('Varun', 'vpass')
    create_admin('Mr. Mendez', 'menPass')
    create_admin('Mr. Bob', 'bobbieboi')
    create_host('Steve','steve')
    create_host('Harvey', 'harvey')

