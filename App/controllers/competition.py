from App.models import Competition
from App.database import db

def create_competition(compName):
    newComp = Competition(compName=compName)
    db.session.add(newComp)
    db.session.commit()
    return newComp

def get_all_comps():
    return Competition.query.all()
