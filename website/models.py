#SQLAlchemy DB - Table Models
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    
    id = db.Column(db.Integer,primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True),default = func.now())
    #timezone allowing us to handle with different timezones
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    #ONE TO MANY Relationship between user and note,
    #One user can have multiple notes.
    user = db.relationship("User",back_populates='notes')




class User(db.Model,UserMixin):

    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(100),unique = True)
    username = db.Column(db.String(25),unique = True)
    password = db.Column(db.String(16))
    notes = db.relationship("Note",back_populates='user')
    img = db.relationship("Img",back_populates = "user")

class Img(db.Model):

    id = db.Column(db.Integer,primary_key = True)
    img = db.Column(db.LargeBinary,nullable = False)
    name = db.Column(db.Text,nullable = False)
    mimetype = db.Column(db.Text,nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    user = db.relationship("User",back_populates='img')