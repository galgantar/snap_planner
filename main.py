from flask import Flask, render_template, session, request, redirect
from database import insert_new_user, check_login, confirm_data, user_is_new, list_database, get_user_data, change_data, email_conformation, confirm_email

app = Flask(__name__)
app.secret_key = "FHCqR4tvmOpgbYHWXtbe"

@app.route("/")
def razred():

    if not session.get("user"):
        return redirect("/login")
    else:
        return render_template("pages/class.html", email=session["user"])

@app.route("/register", methods=["GET", "POST"])
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
            email_conformation(email) #send confirmation link
            return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("pages/login.html")

    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password and check_login(email, password):
            session["user"] = email
            return redirect("/")
        else:
            return render_template("pages/login.html", error="Wrong username or password")

@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("/")

@app.route("/database")
def database():
    seznam = list_database()

    return render_template("pages/database.html", seznam=seznam)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        data = get_user_data(session["user"])
        return render_template("pages/profile.html", data=[data])

    elif request.method == "POST":
        passwords = (request.form.get("password1"), request.form.get("password2"))
        name = request.form.get("name")
        surname = request.form.get("surname")
        number = request.form.get("number")

        if passwords[0] and passwords[0] == passwords[1]:
            change_data(0, session["user"], passwords[0])

        elif name and not confirm_data(name=name):
            change_data(1, session["user"], name)

        elif surname and not confirm_data(surname=surname):
            change_data(2, session["user"], surname)

        elif number and not confirm_data(number=number):
            change_data(3, session["user"], number)
        else:
            data = get_user_data(session["user"])
            return render_template("pages/profile.html", data=[data], error="Wrong data")

        return redirect("/profile")

@app.route("/confirmation/<code>")
def confirmation(code):
    if confirm_email(code):
        return redirect("/profile")
    else:
        return render_template("pages/invalid_confirmation.html")


@app.route("/resend")
def resend():
    email_conformation(session["user"])
    return render_template("pages/resend_confirmation.html", email=session["user"])

if __name__ == "__main__":
    app.run(debug=True)
