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
    return course
    

def list_courses():
    courses = Course.query.all()
    if courses:
        print("Courses:")
        for course in courses:
            print(f"Name: {course.name}")
    else:
        print("No courses found.")
    return courses

def get_course():
    while True:
        courseName = input("Enter a course to search for: ").strip()

        if not courseName:
            print("Search field cannot be empty")
            continue
        break

    course_search = Course.query.filter_by(name=courseName).first()

    if course_search:
        print(f"'{course_search.name}' was found")
    else:
        print(f"'{courseName}' was not found")




