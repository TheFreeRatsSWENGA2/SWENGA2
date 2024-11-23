from werkzeug.security import generate_password_hash
from App.database import db
from App.models import User

class Student(User):
    __tablename__ = 'student'

    # Define the user_id as a foreign key, but also part of the composite primary key
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # This is part of the composite PK
    studentID = db.Column(db.Integer, unique=True, nullable=False)
    studentname = db.Column(db.String(20), nullable=False, unique=True)
    studentPassword = db.Column(db.String(120), nullable=False)

    # Composite primary key: student_id and user_id together form the primary key
    __table_args__ = (
        db.PrimaryKeyConstraint('id', 'studentID'),
    )

    def __init__(self, studentname, studentPassword, studentID):
        super().__init__(studentname,studentPassword)
        self.studentID = studentID
        self.studentname = studentname
        self.studentPassword = generate_password_hash(studentPassword)  # Hash the password

    def __repr__(self):
        return f'User:{self.id}-StudentID:{self.studentID}-StudentName:{self.studentname}'
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)