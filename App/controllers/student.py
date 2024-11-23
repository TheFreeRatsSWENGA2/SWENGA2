from App.models import Student
from App.database import db

def create_student(studentName, password):
    newStudent = Student(studentName=studentName, password=password)
    db.session.add(newStudent)
    db.session.commit()
    return newStudent

def get_student_by_studentname(studentname):
    return Student.query.filter_by(studentname=studentName).first()

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    studentjson = [student.get_json() for student in students]
    return studentjson

def update_student(id, studentName):
    student = get_student(id)
    if student:
        student.studentName = studentName
        db.session.add(student)
        return db.session.commit()
    return None
    