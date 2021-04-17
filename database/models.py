from .db import db
from flask_login import UserMixin

class NAT(db.Document):
    protocol = db.StringField(required=True, unique=False)
    time = db.StringField(required=True, unique=False)
    state = db.StringField(required=True, unique=False)
    src_before = db.StringField(required=True, unique=False)
    dst_before = db.StringField(required=True, unique=False)
    sport_before = db.StringField(required=True, unique=False)
    dport_before = db.StringField(required=True, unique=False)
    src_after = db.StringField(required=True, unique=False)
    dst_after = db.StringField(required=True, unique=False)
    sport_after = db.StringField(required=True, unique=False)
    dport_after = db.StringField(required=True, unique=False)
    code_link = db.StringField(required=True, uniqie=False)

class DB_user(UserMixin, db.Document):
    name = db.StringField(required=True, uniqie=False)
    email = db.StringField(required=True, uniqie=False)
    pasw = db.StringField(required=True, uniqie=False)
