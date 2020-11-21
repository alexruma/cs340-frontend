import os

from flask import Flask, render_template, request, session, redirect
import requests 
from db.connection import connect, execute_query

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    """
    displays homepage 
    """

    # get a bunch of albums from itunes
    response = requests.get("https://itunes.apple.com/search?media=music&entity=album&limit=15&term=rap")
    response = response.json()

    # get list of genres for sidebar menu 
    query = "SELECT GenreName, GenreID FROM Genres"
    connection = connect() 
    genres = execute_query(connection, query)
    
    first_genre_id = genres[0][1]

    # get corresponding albums for first genre 
    connection = connect()
    albums_query = f"""Select Albums.AlbumID, Albums.AlbumName, Artists.ArtistName, 
                Artists.ArtistID, Genres.GenreName FROM Genres
                INNER JOIN Album_Genres ON Genres.GenreID = Album_Genres.GenreID
                INNER JOIN Albums ON Album_Genres.AlbumID = Albums.AlbumID
                INNER JOIN Album_Artists ON Albums.AlbumID = Album_Artists.AlbumID
                INNER JOIN Artists ON Album_Artists.ArtistID = Artists.ArtistID
                WHERE Genres.GenreID = {first_genre_id}"""
    albums = execute_query(connection, albums_query)
 
    connection.close()

    return render_template('index.html', 
        context={ "genres": genres, "albums": albums })

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