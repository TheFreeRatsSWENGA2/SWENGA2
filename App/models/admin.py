from werkzeug.security import generate_password_hash
from App.database import db
from App.models import User

class Admin(User):
    __tablename__ = 'admin'

    # Define the user_id as a foreign key, but also part of the composite primary key
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # This is part of the composite PK
    adminID = db.Column(db.Integer, unique=True, nullable=False)
    adminName = db.Column(db.String(20), nullable=False, unique=True)
    adminPassword = db.Column(db.String(120), nullable=False)

    # Composite primary key: student_id and user_id together form the primary key
    __table_args__ = (
        db.PrimaryKeyConstraint('id', 'adminID'),
    )

    def __init__(self, adminName, adminPassword, adminID):
        super().__init__(adminName, adminPassword)
        self.adminID = adminID
        self.adminName = adminName
        self.adminPassword = generate_password_hash(adminPassword)  # Hash the password

    def __repr__(self):
        return f'User:{self.id}-AdminID:{self.adminID}-Admin Name:{self.adminName}'
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)