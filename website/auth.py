#User Loggin and Signup - Authorization
from flask import Blueprint

auth = Blueprint("auth",__name__)


@auth.route('/login',methods = ["GET","POST"])
def login():

    pass

@auth.route("/sign-up",methods = ["GET","POST"])
def signup():

    pass

@auth.route('/logout')
def logout():

    pass