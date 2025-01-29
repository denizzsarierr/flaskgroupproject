#User Loggin and Signup - Authorization
from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,current_user


auth = Blueprint("auth",__name__)


@auth.route('/login',methods = ["GET","POST"])
def login():

    form = request.form
    
    if request.method == "POST":

        username = form.get('username')
        password = form.get('password')

        user = User.query.filter_by(username = username).first()


        if user:

            if check_password_hash(user.password,password):

                flash("Succesfully Logged In",category="success")
                login_user(user,remember = True)
                #Session will continue until loggingout
                return redirect(url_for("views.home"))
            else:
                flash("Wrong Password",category="danger")
        else:

            flash("User doesn't exist",category="error")

    
    return render_template("login.html",user = current_user)




@auth.route("/sign-up",methods = ["GET","POST"])
def signup():

    return render_template('signup.html')

@auth.route('/logout')
def logout():

    return render_template('home.html')