import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from utility.constants import USERS_TABLE_NAME, JOBS_TABLE_NAME

db = SQLAlchemy()


class UserModel(db.Model):
    __tablename__ = USERS_TABLE_NAME

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __init__(self, email, username, password, role):
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.role = role

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def __repr__(self):
        return 'user: {}'.format(self.username)


class JobModel(db.Model):
    __tablename__ = JOBS_TABLE_NAME

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(50), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    requested_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    token = db.Column(db.Text(), nullable=True)
    token_is_valid = db.Column(db.Boolean(), nullable=False)

    def __init__(self, request_id, role, status, requested_timestamp, token, token_is_valid):
        self.request_id = request_id
        self.role = role
        self.status = status
        self.requested_timestamp = requested_timestamp
        self.token = token
        self.token_is_valid = token_is_valid

    def __repr__(self):
        return 'request_id: {}'.format(self.request_id)
