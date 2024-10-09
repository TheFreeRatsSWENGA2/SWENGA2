from App.database import db
from App.models import Course

def create_course():
    name = input("Enter course name: ")
    course = Course(name=name)
    db.session.add(course)
    db.session.commit()
    print("Course created!")

def list_course():
    courses = Course.query.all() 
    if courses:  
        print("Courses:")
        for course in courses:
            print(f"ID: {course.id}, Name: {course.name}")
    else:
        print("No courses found.")


