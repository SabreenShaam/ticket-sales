from models.model import db, JobModel, RuleModel


def save_job(request_id, requested_timestamp, role, status):
    job = JobModel(request_id, requested_timestamp, role, status)
    db.session.add(job)
    db.session.commit()


def save_rule(role, rule):
    rule = RuleModel(role, rule)
    db.session.add(rule)
    db.session.commit()


def clean_the_rule_table():
    RuleModel.query.delete()


def get_job(request_id):
    return JobModel.query.filter_by(request_id=request_id).first()


def get_rule(role):
    return RuleModel.query.filter_by(role=role).first()


def update_the_job():
    db.session.commit()


def get_rule__(role):
    rule_dict = {
      "premium": "instant",
      "standard": "10 minutes",
      "default": "start of the next day"
    }
    return rule_dict.get(role)
