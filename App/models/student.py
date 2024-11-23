from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Student(db.Model):
    studentID = db.Column(db.Integer, primary_key=True)
    studentName =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, studentName, password):
        self.studentName = studentName
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.studentName
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.studentID} - {self.studentName}>'