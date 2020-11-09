import os

from flask import Flask, render_template, request, session, redirect
import requests 
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    response = requests.get("https://itunes.apple.com/search?media=music&entity=album&limit=15&term=rap")
    response = response.json()
    return render_template('index.html', context={ "albums": response["results"] })

@app.route('/about')
def render_about():
    return render_template('about.html')

@app.route('/cart')
def render_cart():
    return render_template('cart-template.html')

@app.route('/account')
def render_account():
    return render_template('account-template.html')

@app.route('/album/<id>')
def render_album(id):
    return render_template('album-template.html')

@app.route("/edit-account")
def render_edit_account():
    return render_template("edit-account-template.html")

@app.route('/admin')
def render_admin():
    if "admin" not in session or not session["admin"]:
        return render_template("index.html")
    return redirect("/admin/add")

@app.route("/admin/<view>")
def render_admin_add(view):
    if "admin" not in session or not session["admin"]:
        return render_template("index.html")

    if view not in ["add", "edit", "delete", "orders"]:
        view = "add"
    
    return render_template('admin.html', view=view)

@app.route("/create-account")
def render_create_account():
    return render_template("create-account.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        session["logged_in"] = True 
        print(request.form["user"])
        if request.form["user"] == "admin":
            session["admin"] = True 
            return redirect("/admin/add")
        return redirect("/")

@app.route("/logout")
def logout():
    if "logged_in" in session:
        del session["logged_in"]
    if "admin" in session:
        del session["admin"]
    return redirect("/")