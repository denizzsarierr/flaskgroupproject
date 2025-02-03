#User Loggin and Signup - Authorization
from flask import Blueprint,render_template,request,flash,redirect,url_for,Response,send_file
from .models import User,db,Note,Img
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,current_user,login_required,logout_user
from . import models
from werkzeug.utils import secure_filename
from io import BytesIO

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

@auth.route('/delete-account')
@login_required
def delete_account():


    db.session.query(User).filter(User.id == current_user.id).delete()
    db.session.query(Note).filter(Note.user_id == current_user.id).delete()
    db.session.commit()
    return redirect(url_for('auth.sign_up'))


@auth.route('/upload',methods = ["POST"])
@login_required
def upload():

    pic = request.files['pic']

    if not pic:

        return redirect(url_for('views.profile'))
    
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype

    img = Img(img=pic.read(),mimetype = mimetype,name = filename)
    db.session.add(img)
    db.session.flush()

    if current_user.img:
        old_image = current_user.img[0]
        db.session.delete(old_image)

    current_user.img = [img]
    
    db.session.commit()

    return redirect(url_for('views.home'))


@auth.route('/image/<int:id>')
def get_img(id):

    img = Img.query.get(id)

    if img:
    
        image_data = BytesIO(img.img)
        image_data.seek(0)
        return send_file(image_data, mimetype=img.mimetype)
    else:
        return send_file('static/default-profile.jpg', mimetype='image/jpg')
    


