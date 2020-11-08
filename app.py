import os

from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        session["admin"] = True 
        return render_template("admin.html")

@app.route("/logout")
def logout():
    if "admin" in session:
        del session["admin"]
    return redirect("/")