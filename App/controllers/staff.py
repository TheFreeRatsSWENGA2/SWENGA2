from App.database import db
from App.models import Staff
from flask import request, jsonify, has_request_context

def create_staff():
    # Determine if we're in Flask context
    if has_request_context():  # Check if we're inside an HTTP request context
        data = request.get_json()
        name = data.get("name", "").strip()
        role = data.get("role", "").strip()
    else:  # Terminal input if not in Flask context
        name = input("Enter staff name: ").strip()
        role = input("Enter staff role: ").strip()

    # Validate staff name
    while True:
        if not name:
            if has_request_context():
                return jsonify({"error": "Staff name cannot be empty!"}), 400
            else:
                print("Staff name cannot be empty!")
                name = input("Enter staff name: ").strip()
                continue

        existing_staff = Staff.query.filter_by(name=name).first()
        if existing_staff:
            if has_request_context():
                return jsonify({"error": f"Staff '{name}' already exists. Please enter a different name."}), 409
            else:
                print(f"Staff '{name}' already exists. Please enter a different name.")
                name = input("Enter staff name: ").strip()
                continue
        break

    # Validate staff role
    while True:
        if not role:
            if has_request_context():
                return jsonify({"error": "Staff role cannot be empty!"}), 400
            else:
                print("Staff role cannot be empty!")
                role = input("Enter staff role: ").strip()
                continue
        break

    # Create and save the new staff member
    staff = Staff(name=name, role=role)
    db.session.add(staff)
    db.session.commit()

    success_message = f'Staff Created! Staff ID: {staff.id}'

    if has_request_context():
        return jsonify({"message": success_message, "staff": {"id": staff.id, "name": staff.name, "role": staff.role}}), 201
    else:
        print(success_message)
        return staff




def list_staff():
    staff_members = Staff.query.all()
    
    if staff_members:
        print("Staff Members:")
        for staff in staff_members:
            print(f"ID: {staff.id}, Name: {staff.name}, Role: {staff.role}")
    else:
        print("No staff members found.")
