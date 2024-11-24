from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Competition(db.Model):
    competitionID = db.Column(db.Integer, primary_key=True)
    compName =  db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, compName):
        self.compName = compName

    # def get_json(self):
    #     return{
    #         'id': self.id,
    #         'username': self.username
    #     }
    
    def __repr__(self):
        return f'CompetitionID:{self.competitionID}-CompetitionName:{self.compName}'