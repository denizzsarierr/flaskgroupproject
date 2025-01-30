#Route
from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from flask_login import current_user,login_required
from .models import Note
from . import models,db
import json


views = Blueprint("views",__name__)

@views.route('/',methods = ["GET","POST"])
@login_required
def home():

    form = request.form
    notes = Note.query.all()
    #Return all the values

    if request.method == "POST":
        note = form.get("note")
        
        if len(note) > 0:
            
            existing_note = Note.query.filter_by(data=note).first()

            if existing_note:
                flash("This note is already exist",category="error")
            
            else:

                new_note = models.Note(data = note,user_id = current_user.id)

                db.session.add(new_note)
                db.session.commit()

                flash("Note Added",category="success")
                return redirect(url_for('views.home'))
    return render_template("home.html",user = current_user,notes=notes)

@views.route("/delete-note",methods = ["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)

    if note:

        if note.user_id == current_user.id:
            ##we are checking if it is correct user
            db.session.delete(note)
            db.session.commit()
        else:
            flash("You do not have permission for this.","error")
    
    return jsonify({})
@views.route('/profile',methods = ["GET","POST"])
@login_required
def profile():

    if request.method == "POST":

        return redirect(url_for('views.mynotes'))
        
        



    return render_template('profile.html',user = current_user)

@views.route('/mynotes',methods = ["GET","POST"])
@login_required
def mynotes():

    if request.method == "POST":
        pass


    return render_template("mynotes.html",user = current_user)


