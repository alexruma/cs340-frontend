import os

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about.html')
def render_about():
    return render_template('about.html')

@app.route('/cart-template.html')
def render_cart():
    return render_template('cart-template.html')

@app.route('/account-template.html')
def render_account():
    return render_template('account-template.html')

@app.route('/album-template.html')
def render_album():
    return render_template('album-template.html')
   
@app.route('/admin.html')
def render_admin():
    return render_template('admin.html')
