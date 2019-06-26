from flask import Flask, render_template, request, redirect, make_response
import database
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

        if not database.user_is_new(email):
            return render_template("pages/register.html", error="Account already exists")

        data_validation = database.confirm_data(name, surname, email, number)

        if data_validation:
            return render_template("pages/register.html", error=data_validation)

        else:
            database.insert_new_user(name, surname, password, email, number)
            database.email_conformation(email) #send confirmation link
            return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("pages/login.html")

    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password and database.check_login(email, password):
            response = make_response(redirect("/"))
            expiration_date = int(time.time()) + 24*3600* 365 #Cookies valid for 365 days
            response.set_cookie("user", email, expires=expiration_date)
            return response
        else:
            return render_template("pages/login.html", error="Wrong username or password")

@app.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.set_cookie("user", "", expires=0) #Cookie will become expired immediately
    return response

@app.route("/database")
def list_database():
    if request.cookies.get("user"):
        data = database.list_database()
        return render_template("pages/database.html", data=data)
    else:
        return redirect("/")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    email = request.cookies.get("user")
    if not email:
        return redirect("/login")

    if request.method == "GET":
        data = database.get_user_data(email)
        return render_template("pages/profile.html", data=data)

    elif request.method == "POST":
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        name = request.form.get("name")
        surname = request.form.get("surname")
        number = request.form.get("number")

        if password1 and password2 and password1 == password2:
            database.change_data(0, email, password1)

        elif name and not database.confirm_data(name=name):
            database.change_data(1, email, name)

        elif surname and not database.confirm_data(surname=surname):
            database.change_data(2, email, surname)

        elif number and not database.confirm_data(number=number):
            database.change_data(3, email, number)
        else:
            data = database.get_user_data(email)
            return render_template("pages/profile.html", data=data, error="Wrong data")

        return redirect("/profile")

@app.route("/confirmation")
def incomplete_confirmation():
    return redirect("/login")

@app.route("/confirmation/<code>")
def confirmation(code):
    if database.confirm_email(code):
        return redirect("/profile")
    else:
        return render_template("pages/invalid_confirmation.html")


@app.route("/resend")
def resend():
    email = request.cookies.get("user")
    if email:
        database.email_conformation(email)
        return render_template("pages/resend_confirmation.html", email=email)
    else:
        return redirect("/")

@app.route("/password", methods=["GET", "POST"])
def password():
    if request.method == "GET":
        return render_template("pages/password.html")

    elif request.method == "POST":
        email = request.form.get("email")

        if email:
            database.reset_password(email)

        return redirect("/login")

@app.route("/password/<code>", methods=["GET", "POST"])
def new_password(code):
    email = request.args.get("email").replace("<at>", "@")

    if not email or not database.user_in_database(email):
        return redirect("/login")

    if request.method == "GET":
        return render_template("pages/new_password.html", email=email)

    elif request.method == "POST":
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 == password2 and database.check_password_code(email, code):
            database.change_data(0, email, password1)
            return redirect("/login")

        else:
            return render_template("pages/new_password.html", email=email, error="Expired or incorrect link")

@app.route("/timetables")
def timetables():
    if request.cookies.get("user"):
        data = database.get_timetables()
        return render_template("pages/timetables.html", data=data)
    else:
        return redirect("/")

@app.route("/timetables/new", methods=["GET", "POST"])
def add_timetable():
    email = request.cookies.get("user")
    if not email:
        return redirect("/login")

    if request.method == "GET":
        return render_template("pages/new_timetable.html")

    elif request.method == "POST":
        name = request.form.get("name")
        days = request.form.getlist("day")

        if len(name) > 30:
            return render_template("pages/new_timetable.html", error="Name must be shorter than 30")
        if not days:
            return render_template("pages/new_timetable.html", error="You must add at least one weekday")

        all_days = ["mon", "tue", "wed", "thu", "fri"]
        days_binary = []
        for day in all_days:
            if day in days:
                days_binary.append("1")
            else:
                days_binary.append("0")

        database.new_timetable(name, days_binary, request.cookies.get("user"))

        return redirect("/timetables")

@app.route("/timetable/<name>", methods=["GET", "POST"])
def table(name, error=None):
    email = request.cookies.get("user")
    if not email:
        return redirect("/login")

    if request.method == "GET":
        data = database.get_timetable_data(name, email)
        if not data:
            return redirect("/timetables")
        dates_array = data[0]
        myDate = data[1]
        return render_template("pages/timetable.html", name=name, data=dates_array, myDate=myDate)

    elif request.method == "POST":
        date_to_add = request.form.get("add-date")
        date_to_remove = request.form.get("remove-date")
        
        if date_to_add:
            error = database.add_date(email, date_to_add, name)
        elif date_to_remove:
            database.remove_date(email, date_to_remove, name)
        else:
            error = "Incomplete data post request"

        if error:
            data = database.get_timetable_data(name, email)
            dates_array = data[0]
            myDate = data[1]
            return render_template("pages/timetable.html", name=name, data=dates_array, myDate=myDate, error=error)
        else:
            return redirect("/timetable/{}".format(name))

@app.route("/mydates")
def mydates():
    email = request.cookies.get("user")
    if not email:
        return redirect("/login")

    data = database.get_my_dates(email)

    return render_template("pages/my_dates.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
