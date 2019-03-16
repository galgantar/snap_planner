from flask import Flask, render_template, session, request, redirect

app = Flask(__name__)
app.secret_key = "adadasjfa"
users = {"Gal":"asuna","Test":"asuna", "Vid":"asuna"}

@app.route("/")
def index():
    if not session.get("user"):
        return redirect("/login")
    else:
        return render_template("index.html", username=session["user"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Wrong password or username")

@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
