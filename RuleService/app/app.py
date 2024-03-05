from flask import Flask
from flask_jwt_extended import JWTManager

from config import JWT_SECRET_KEY, DB_ENGINE
from models.model import db
from service.consumer import consume_request_from_kafka
from utility.db_script import add_rules_in_to_the_db

app = Flask(__name__)

jwt = JWTManager()

# app.config['SQLALCHEMY_DATABASE_URI'] = DB_ENGINE
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db_rules/ticket_rules'
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
jwt.init_app(app)
db.init_app(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_rules_in_to_the_db()
        consume_request_from_kafka()
        app.run(host='0.0.0.0', port=5001)
