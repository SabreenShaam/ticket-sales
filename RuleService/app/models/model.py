import datetime

from flask_sqlalchemy import SQLAlchemy

from utility.constants import USERS_TABLE_NAME, JOBS_TABLE_NAME, RULES_TABLE_NAME

db = SQLAlchemy()


class JobModel(db.Model):
    __tablename__ = JOBS_TABLE_NAME

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(50), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    requested_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, request_id, requested_timestamp, role, status):
        self.request_id = request_id
        self.requested_timestamp = requested_timestamp
        self.role = role
        self.status = status

    def __repr__(self):
        return 'request_id: {}'.format(self.request_id)


class RuleModel(db.Model):
    __tablename__ = RULES_TABLE_NAME

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(255), nullable=False, unique=True)
    rule = db.Column(db.String(255), nullable=False)

    def __init__(self, role, rule):
        self.role = role
        self.rule = rule

    def __repr__(self):
        return 'role: {}'.format(self.role)
