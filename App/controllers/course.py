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


def list_staff():
    staff_members = Staff.query.all()
    
    if not staff_members:
        return jsonify({"message": "No staff members found."}), 404

    staff_list = []
    for staff in staff_members:
        staff_list.append({
            "id": staff.id,
            "name": staff.name,
            "role": staff.role
        })

    return jsonify({"staff": staff_list}), 200



