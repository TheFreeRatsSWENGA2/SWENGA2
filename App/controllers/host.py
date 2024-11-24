from App.models import Host
from App.database import db


def generate_id():
    # Get the highest student_id from the student table
    max_id = db.session.query(db.func.max(Host.hostID)).scalar()
    
    # If there are no students, start at 1
    if max_id is None:
        return 1
    else:
        # Otherwise, increment the highest student_id by 1
        return max_id + 1

def create_host(hostName, password):
    hostID = generate_id()
    newhost = Host(hostID=hostID, hostName=hostName, hostPassword=password)
    db.session.add(newhost)
    db.session.commit()
    return newhost

def get_all_hosts():
    return Host.query.all()

def host_competition():
    hostedComp = create_competitionHost(competitionID, hostID)
    return hostedComp
