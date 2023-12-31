from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.party_model import Party
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)


# ? ========== LOGIN / REGISTER PAGE - VIEW =========
@app.route("/")
def index():
    return render_template("index.html")


# ? ========= REGISTER - method - ACTION ========
@app.route("/user/register", methods=["post"])
def user_reg():
    print(request.form)
    if not User.validate(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    data = {**request.form, "password": pw_hash}
    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect("/dashboard")


# ? ----------- LOGIN - methods - action
@app.route("/user/login", methods=["post"])
def user_login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("invalid credentials")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("invalid credentials")
        return redirect("/")

    session["user_id"] = user_in_db.id
    return redirect("/dashboard")


# ?------------ DASHBOARD PAGE - RENDER -----------
@app.route("/dashboard")
def dash():
    if "user_id" not in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    logged_user = User.get_by_id(data)
    all_party = Party.get_all_user()
    return render_template(
        "dashboard.html", logged_user=logged_user, all_party=all_party
    )


# ?------ LOGOUT ------ action
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
