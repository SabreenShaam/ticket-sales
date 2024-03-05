from models.model import db, UserModel, JobModel
from utility.constants import DEFAULT_ROLE, PENDING_STATUS


def search_uname(username):
    return UserModel.query.filter_by(username=username).first()


def get_job(request_id):
    return JobModel.query.filter_by(request_id=request_id).first()


def update_the_job():
    db.session.commit()


def get_user(user_id):
    return UserModel.query.filter_by(id=user_id).first()


def save_user(email, username, password, role):
    user = UserModel(email=email, username=username, password=password, role=role)
    db.session.add(user)
    db.session.commit()


def store_the_user_request(request_id, requested_timestamp, role=DEFAULT_ROLE):
    request_id = request_id
    role = role
    status = PENDING_STATUS
    token = None
    token_is_valid = False
    requested_timestamp = requested_timestamp
    job = JobModel(request_id=request_id, role=role, status=status, requested_timestamp=requested_timestamp,
                   token=token, token_is_valid=token_is_valid)
    db.session.add(job)
    db.session.commit()
