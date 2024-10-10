from flask import Blueprint, request, jsonify
from App.database import db
from App.models import Course, Staff, Assignment

course_views = Blueprint('course_views', __name__)


@course_views.route('/test', methods=['GET'])
def test():
    return jsonify(message='course.py working')

@course_views.route('/create_course', methods=['POST'])
def create_course_view():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "Course name is required"}), 400
    course = Course(name=name)
    db.session.add(course)
    db.session.commit()
    return jsonify({"message": "Course created!", "course_name": course.name}), 201

@course_views.route('/create_staff', methods=['POST'])
def create_staff_view():
    data = request.get_json()
    name = data.get('name')
    role = data.get('role')
    if not name or not role:
        return jsonify({"error": "Staff name and role are required"}), 400
    staff = Staff(name=name, role=role)
    db.session.add(staff)
    db.session.commit()
    return jsonify({"message": "Staff created!", "staff_id": staff.id}), 201

@course_views.route('/assign_staff', methods=['POST'])
def assign_staff_view():
    data = request.get_json()
    course_name = data.get('course_name')
    staff_id = data.get('staff_id')
    course = Course.query.get(course_name)
    staff = Staff.query.get(staff_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    if not staff:
        return jsonify({"error": "Staff not found"}), 404
    assignment = Assignment(course_name=course_name, staff_id=staff_id)
    db.session.add(assignment)
    db.session.commit()
    return jsonify({"message": f"Staff {staff.name} assigned to course {course.name}"}), 200

@course_views.route('/view_course_staff/<course_name>', methods=['GET'])
def view_course_staff_view(course_name):
    course = Course.query.get(course_name)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    staff_list = []
    for assignment in course.assignments:
        staff = Staff.query.get(assignment.staff_id)
        staff_list.append({"name": staff.name, "role": staff.role})
    return jsonify({"course_name": course.name, "staff": staff_list}), 200


@course_views.route('/list_staff', methods=['GET'])
def list_staff_view():
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
