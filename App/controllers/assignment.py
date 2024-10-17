from App.database import db
from App.models import Staff
from App.models import Course
from App.models import Assignment

def assign_staff():
    while True:
        course_name = input("Enter course name: ").strip()

        existingCourse = Course.query.filter_by(name=course_name).first()

        if not existingCourse:
            print("Course does not exist")
        
        else:

            if not course_name:
                print("Course name cannot be empty!")
                continue

            break

    while True:
        staff_id = input("Enter staff ID: ").strip()

        existingStaff = Staff.query.filter_by(id=staff_id).first()

        if not existingStaff:
            print("Staff member does not exist")


        else:

            if not staff_id:
                print("Staff ID cannot be empty!")
                continue
                
            break

    assignment = Assignment(course_name=course_name, staff_id=staff_id)
    db.session.add(assignment)
    db.session.commit()
    print(f'Staff member: {assignment.id}: ({existingStaff.name}) assigned to: {assignment.course_name}')
    return assignment

def view_course_staff():
    while True:
        name = input("Enter course Name: ").strip()
        course = Course.query.filter_by(name=name).first()
        if not course:
            print("Course not found.")
            continue

        print(f'Staff for Course {course.name}: ')

        for assignment in course.assignments:
            staff = Staff.query.get(assignment.staff_id)
            print(f'{staff.name} - {staff.role}')

        break
    