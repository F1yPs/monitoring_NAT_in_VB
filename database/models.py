from .db import db

class NAT(db.Document):
    track_id = db.IntField()
    protocol = db.StringField(required=True, unique=False)
    time = db.StringField(required=True, unique=False)
    src_before = db.StringField(required=True, unique=False)
    dst_before = db.StringField(required=True, unique=False)
    sport_before = db.StringField(required=True, unique=False)
    dport_before = db.StringField(required=True, unique=False)
    src_after = db.StringField(required=True, unique=False)
    dst_after = db.StringField(required=True, unique=False)
    sport_after = db.StringField(required=True, unique=False)
    dport_after = db.StringField(required=True, unique=False)
    code_link = db.StringField(required=True, uniqie=False)

