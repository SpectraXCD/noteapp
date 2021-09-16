from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import *
from . import db
import json

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short.", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added.", category="success")
    return render_template("home.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route("/users", methods=["GET", "POST"])
@login_required
def users():
    return render_template("users.html", user=current_user, users=User.query.all())


@views.route("/users/delete-user", methods=["POST"])
def delete_user():
    user = json.loads(request.data)
    print(request.data)
    userId = user["userId"]
    user = User.query.get(userId)
    if user:
        db.session.delete(user)
        db.session.commit()

    return jsonify({})
