from App.database import db
from App.models import Staff
from App.models import Course
from App.models import Assignment
from flask import request, jsonify, has_request_context

def assign_staff():
    # Determine if we're in Flask context
    if has_request_context():  # This will check if we're in an HTTP request context
        data = request.get_json()
        course_name = data.get("course_name")
        staff_name = data.get("staff_name")
    else:  # If not in Flask context, use terminal input
        course_name = input("Enter course name: ").strip()
        staff_name = input("Enter staff name: ").strip()

    # Input and validate course name
    existingCourse = Course.query.filter_by(name=course_name).first()
    if not existingCourse:
        message = "Course does not exist."
        if has_request_context():
            return jsonify({"error": message}), 404
        else:
            print(message)
            return None

    # Input and validate staff name
    existingStaff = Staff.query.filter_by(name=staff_name).first()
    if not existingStaff:
        message = "Staff member does not exist."
        if has_request_context():
            return jsonify({"error": message}), 404
        else:
            print(message)
            return None

    # Check if the staff member (by name) is already assigned to the course
    existingAssignment = db.session.query(Assignment).join(Staff).filter(
        Assignment.course_name == course_name, 
        Staff.name == staff_name
    ).first()

    if existingAssignment:
        message = f"Staff member {existingStaff.name} is already assigned to the course {course_name}."
        if has_request_context():
            return jsonify({"error": message}), 400
        else:
            print(message)
            return None

    # Proceed with assigning the staff if no duplicate found
    assignment = Assignment(course_name=course_name, staff_id=existingStaff.id)
    db.session.add(assignment)
    db.session.commit()

    success_message = f'Staff member {existingStaff.name} successfully assigned to the course {course_name}.'
    
    if has_request_context():
        return jsonify({"message": success_message}), 200
    else:
        print(success_message)
        return assignment  # Return the assignment object for further verification





def view_course_staff():
    # Determine if we're in Flask context
    if has_request_context():  # Check if we're inside an HTTP request context
        data = request.get_json()
        course_name = data.get("name", "").strip()
    else:  # Terminal input if not in Flask context
        course_name = input("Enter course Name: ").strip()

    # Validate course name
    while True:
        if not course_name:
            if has_request_context():
                return jsonify({"error": "Course name cannot be empty!"}), 400
            else:
                print("Course name cannot be empty!")
                course_name = input("Enter course Name: ").strip()
                continue

        # Retrieve course by name
        course = Course.query.filter_by(name=course_name).first()
        if not course:
            if has_request_context():
                return jsonify({"error": "Course not found."}), 404
            else:
                print("Course not found.")
                course_name = input("Enter course Name: ").strip()
                continue
        break

    # Fetch staff assignments for the course
    staff_list = []
    for assignment in course.assignments:
        staff = Staff.query.get(assignment.staff_id)
        staff_info = {"name": staff.name, "role": staff.role}
        staff_list.append(staff_info)

    # Handle output for Flask or terminal
    if has_request_context():
        return jsonify({
            "course": course.name,
            "staff": staff_list
        }), 200
    else:
        print(f'Staff for Course {course.name}: ')
        for staff in staff_list:
            print(f'{staff["name"]} - {staff["role"]}')
        return staff_list


# def list_staff():
#     staff_members = Staff.query.all()
    
#     if not staff_members:
#         return jsonify({"message": "No staff members found."}), 404

#     staff_list = []
#     for staff in staff_members:
#         staff_list.append({
#             "id": staff.id,
#             "name": staff.name,
#             "role": staff.role
#         })

#     print(f"ID: {staff.id}, Name: {staff.name}, Role: {staff.role}")
#     return jsonify({"staff": staff_list}), 200
    



def list_staff():
    staff_members = Staff.query.all()


    if request:
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

    # Terminal context (No `request` object)
    else:
        if not staff_members:
            print("No staff members found.")
            return

        for staff in staff_members:
            print(f"ID: {staff.id}, Name: {staff.name}, Role: {staff.role}")

