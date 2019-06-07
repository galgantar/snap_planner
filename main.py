from flask import Flask, render_template, session, request, redirect
from database import insert_new_user, check_login, confirm_data, user_is_new, list_database

app = Flask(__name__)
app.secret_key = "FHCqR4tvmOpgbYHWXtbe"

@app.route("/")
def index():
    return render_template("pages/index.html")

@app.route("/razred")
def razred():

    if not session.get("user"):
        return redirect("/razred/login")
    else:
        return render_template("pages/class.html", email=session["user"])

@app.route("/razred/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("pages/register.html")

    elif request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        number = request.form.get("number")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if not (name and surname and email and number and password):
            return render_template("pages/register.html", error="All fields are mandatory")

        if not password == password2:
            return render_template("pages/register.html", error="Passwords do not match")

        data_validation = confirm_data(name, surname, email, number)
        is_new = user_is_new(email)
        if data_validation:
            return render_template("pages/register.html", error=data_validation)
        elif is_new:
            return render_template("pages/register.html", error=is_new)
        else:
            insert_new_user(name, surname, password, email, number)
            return redirect("/razred/login")

@app.route("/razred/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("pages/login.html")

    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password and check_login(email, password):
            session["user"] = email
            return redirect("/razred")
        else:
            return render_template("pages/login.html", error="Wrong username or password")

@app.route("/razred/logout")
def logout():
    session["user"] = None
    return redirect("/razred")

@app.route("/razred/database")
def database():
    seznam = list_database()

    return render_template("pages/database.html", seznam=seznam)

if __name__ == "__main__":
    app.run(debug=True)
