#User Loggin and Signup - Authorization
from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User,db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,current_user,login_required,logout_user
from . import models

auth = Blueprint("auth",__name__)


@auth.route('/login',methods = ["GET","POST"])
def login():

    form = request.form

    if request.method == "POST":

            username = form.get('username')
            password = form.get('password1')

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




@auth.route('/sign-up',methods = ["GET","POST"])
def sign_up():

    form = request.form
    
    if request.method == "POST":
        email = form.get("email")
        username = form.get("username")
        password1 = form.get("password1")
        password2 = form.get("password2")

        if len(email) > 0 and len(username) > 0 and len(password1) > 0 and len(password2) > 0:
            new_user = models.User(email=email,username=username,password = generate_password_hash(password1,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Account Created",category="success")
            return redirect(url_for('views.home'))





    return render_template('signup.html',user = current_user)

@auth.route('/logout',methods = ["GET","POST"])
@login_required
def logout():

    logout_user()
    return redirect(url_for('auth.login'))