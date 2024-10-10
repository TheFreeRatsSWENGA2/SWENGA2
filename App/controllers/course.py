from App.database import db
from App.models import Course

def create_course():
    while True:
        name = input("Enter course name: ").strip()

        if not name:
            print("Course name cannot be empty!")
            continue

        existing_course = Course.query.filter_by(name=name).first()
        if existing_course:
            print(f"Course '{name}' already exists. Please enter a different name.")
            continue 

        break

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


