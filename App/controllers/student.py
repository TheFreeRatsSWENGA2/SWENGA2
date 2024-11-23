from App.models import Student
from App.database import db

def generate_id():
    # Get the highest student_id from the student table
    max_id = db.session.query(db.func.max(Student.studentID)).scalar()
    
    # If there are no students, start at 1
    if max_id is None:
        return 1
    else:
        # Otherwise, increment the highest student_id by 1
        return max_id + 1

def create_student(studentname, password):
    studentID = generate_id()
    newstudent = Student(studentID=studentID, studentname=studentname, studentPassword=password)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def get_all_students():
    return Student.query.all()
