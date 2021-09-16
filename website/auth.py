from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Login success.", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Login failure. Incorrect username/password.", category="error")
        else:
            flash("This username does not exist.", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        userWithExistingEmail = User.query.filter_by(email=email).first()
        userWithExistingUsername = User.query.filter_by(username=username).first()
        if userWithExistingUsername:
            flash("Username already in use.", category="error")
        elif userWithExistingEmail:
            flash("Email already in use.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(name) < 2:
            flash("Name must be greater than 1 character.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            new_user = User(
                username=username,
                email=email,
                name=name,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(f"Account created. Welcome, {username}.", category="success")
            return redirect(url_for("views.home"))
    return render_template("signup.html", user=current_user)
