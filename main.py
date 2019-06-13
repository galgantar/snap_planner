from flask import Flask, render_template, request, redirect, make_response
from database import insert_new_user, check_login, confirm_data, user_is_new, list_database, get_user_data, change_data, email_conformation, confirm_email
import os, time

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

@app.route("/")
def razred():
    email = request.cookies.get("user")
    if not email:
        return redirect("/login")
    else:
        return render_template("pages/class.html", email=email)

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
            response = make_response(redirect("/"))
            expiration_date = int(time.time()) + 365*24*3600 #Cookies valid for 365 days
            response.set_cookie("user", email, expires=expiration_date)
            return response
        else:
            return render_template("pages/login.html", error="Wrong username or password")

@app.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.set_cookie("user", "", expires=0) #Cookie will be expired immediately
    return response

@app.route("/database")
def database():
    if request.cookies.get("user"):
        seznam = list_database()
        return render_template("pages/database.html", seznam=seznam)
    else:
        return redirect("/")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        email = request.cookies.get("user")
        if email:
            data = get_user_data(email)
            return render_template("pages/profile.html", data=[data])
        else:
            return redirect("/")

    elif request.method == "POST":
        email = request.cookies.get("user")
        if email:
            passwords = (request.form.get("password1"), request.form.get("password2"))
            name = request.form.get("name")
            surname = request.form.get("surname")
            number = request.form.get("number")

            if passwords[0] and passwords[0] == passwords[1]:
                change_data(0, email, passwords[0])

            elif name and not confirm_data(name=name):
                change_data(1, email, name)

            elif surname and not confirm_data(surname=surname):
                change_data(2, email, surname)

            elif number and not confirm_data(number=number):
                change_data(3, email, number)
            else:
                data = get_user_data(email)
                return render_template("pages/profile.html", data=[data], error="Wrong data")

            return redirect("/profile")
        else:
            return redirect("/") # Sender not logged in

@app.route("/confirmation/<code>")
def confirmation(code):
    if confirm_email(code):
        return redirect("/profile")
    else:
        return render_template("pages/invalid_confirmation.html")


@app.route("/resend")
def resend():
    email = request.cookies.get("user")
    if email:
        email_conformation(email)
        return render_template("pages/resend_confirmation.html", email=email)
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
