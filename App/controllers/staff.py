from App.database import db
from App.models import Staff

def create_staff():
    name = input("Enter staff name: ")
    role = input("Enter staff role: ")
    staff = Staff(name=name, role=role)
    db.session.add(staff)
    db.session.commit()
    print(f'Staff Created! Staff ID:{staff.id}')



def list_staff():
    staff_members = Staff.query.all()
    
    if staff_members:
        print("Staff Members:")
        for staff in staff_members:
            print(f"ID: {staff.id}, Name: {staff.name}, Role: {staff.role}")
    else:
        print("No staff members found.")
