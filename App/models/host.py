from werkzeug.security import generate_password_hash
from App.database import db
from App.models import User

class Host(User):
    __tablename__ = 'host'

    # Define the user_id as a foreign key, but also part of the composite primary key
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # This is part of the composite PK
    hostID = db.Column(db.Integer, unique=True, nullable=False)
    hostName = db.Column(db.String(20), nullable=False, unique=True)
    hostPassword = db.Column(db.String(120), nullable=False)

    # Composite primary key: student_id and user_id together form the primary key
    __table_args__ = (
        db.PrimaryKeyConstraint('id', 'hostID'),
    )

    def __init__(self, hostName, hostPassword, hostID):
        super().__init__(hostName, hostPassword)
        self.hostID = hostID
        self.hostName = hostName
        self.hostPassword = generate_password_hash(hostPassword)  # Hash the password

    def __repr__(self):
        return f'User:{self.id}-hostID:{self.hostID}-hostName:{self.hostName}'
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)