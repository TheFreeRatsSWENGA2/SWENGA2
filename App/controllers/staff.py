from App.database import db
from App.models import Staff

def create_staff():
    while True:
        name = input("Enter staff name: ").strip()

        if not name:
            print("Staff name cannot be empty!")
            continue

        existing_staff = Staff.query.filter_by(name=name).first()
        if existing_staff:
            print(f"Staff '{name}' already exists. Please enter a different name.")
            continue 

        break

    while True:
        role = input("Enter staff role: ").strip()
        if not role:
            print("Staff roll cannot be empty!")
            continue
            
        break

    staff = Staff(name=name, role=role)
    db.session.add(staff)
    db.session.commit()
    print(f'Staff Created! Staff ID:{staff.id}')
    return staff



def list_staff():
    staff_members = Staff.query.all()
    
    if staff_members:
        print("Staff Members:")
        for staff in staff_members:
            print(f"ID: {staff.id}, Name: {staff.name}, Role: {staff.role}")
    else:
        print("No staff members found.")
