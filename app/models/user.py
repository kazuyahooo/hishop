from flask_login import UserMixin
import datetime

from app import db, login_manager

class Address(db.EmbeddedDocument):
	address = db.StringField(required=True, max_length=50)

class User(UserMixin, db.Document):
    account = db.StringField(required=True, unique=True, min_length=4, max_length=20)
    password = db.StringField(required=True)
    name = db.StringField(required=True, max_length=50)
    icon = db.StringField(required=True, default="default.png")
    email = db.StringField(required=True, unique=True)
    phone = db.StringField(required=True, max_length=15)
    birth = db.DateTimeField(required=True)
    address = db.ListField(db.EmbeddedDocumentField(Address), default=list)
    hicoin = db.LongField(required=True, default=0)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow())
    
@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()