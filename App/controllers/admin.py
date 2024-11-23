from App.models import Admin
from App.database import db

def generate_id():
    # Get the highest student_id from the student table
    max_id = db.session.query(db.func.max(Admin.adminID)).scalar()
    
    # If there are no students, start at 1
    if max_id is None:
        return 1
    else:
        # Otherwise, increment the highest student_id by 1
        return max_id + 1

def create_admin(adminName, password):
    adminID = generate_id()
    newadmin = Admin(adminID=adminID, adminName=adminName, adminPassword=password)
    db.session.add(newadmin)
    db.session.commit()
    return newadmin

def get_all_admins():
    return Admin.query.all()
