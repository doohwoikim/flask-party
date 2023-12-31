from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user_model import User
from flask_app.models.party_model import Party


# ? ================= CREATE  render==================
@app.route("/parties/new")
def new_party():
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": session["user_id"]}
    logged_user = User.get_by_id(data)
    return render_template("new.html", logged_user=logged_user)


# ? =========== CREATE - method - ACTION
@app.route("/parties/register", methods=["POST"])
def create_party():
    if "user_id" not in session:
        return redirect("/logout")
    if not Party.parties_validate(request.form):
        return redirect("/parties/new")
    party_data = {
        "name": request.form["name"],
        "descriptions": request.form["descriptions"],
        "instructions": request.form["instructions"],
        "created_at": request.form["created_at"],
        "under": request.form["under"],
        "user_id": session["user_id"],
    }
    Party.create(party_data)
    return redirect("/dashboard")


# ? ========== READ ONE - RENDER
@app.route("/parties/<int:id>")
def show_party(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": session["user_id"]}
    user_data = {"id": id}
    logged_user = User.get_by_id(data)
    logged_party = Party.get_one_user(user_data)
    return render_template(
        "show.html", logged_user=logged_user, logged_party=logged_party
    )


# ? ============ UPDATE - RENDER -page
@app.route("/parties/edit/<int:id>")
def edit_party(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": session["user_id"]}
    user_data = {"id": id}
    logged_user = User.get_by_id(data)
    logged_party = Party.get_by_id(user_data)
    return render_template(
        "edit.html", logged_user=logged_user, logged_party=logged_party
    )


# ? =========== Edit - method - ACTION
@app.route("/parties/edit/<int:id>", methods=["POST"])
def update_party(id):
    if not Party.parties_validate(request.form):
        return redirect(f"/parties/edit/{id}")
    party_data = {**request.form}
    Party.update(party_data)
    return redirect("/dashboard")


# ? ========== DELETE - ACTION
@app.route("/parties/delete/<int:id>")
def delete_party(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": session["user_id"]}
    user_data = {"id": id}
    User.delete(data)
    Party.delete(user_data)
    return redirect("/dashboard")
