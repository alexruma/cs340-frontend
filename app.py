import os

from flask import Flask, render_template, request, session, redirect, jsonify
import requests 
from db.connection import connect, execute_query, insert_data, update_data

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

## Think it would be good to have queries in another file as functions that take in the parameters to complete them


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
                Artists.ArtistID, Genres.GenreName, Albums.Price FROM Genres
                INNER JOIN Album_Genres ON Genres.GenreID = Album_Genres.GenreID
                INNER JOIN Albums ON Album_Genres.AlbumID = Albums.AlbumID
                INNER JOIN Album_Artists ON Albums.AlbumID = Album_Artists.AlbumID
                INNER JOIN Artists ON Album_Artists.ArtistID = Artists.ArtistID
                WHERE Genres.GenreID = {first_genre_id}"""
    albums = execute_query(connection, albums_query)
    print(albums)
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
    connection = connect()
    user_id = session["user_id"]
    # get user info to display, user favGenreID to get genre name 
    query = f"""select firstName, lastName, email, GenreName from Customers
                INNER JOIN Genres ON Customers.favGenre = Genres.GenreID
                where CustomerID = {user_id} """
    user = execute_query(connection, query)
    firstName, lastName, email, favGenre = user[0]
  
    query = f"""SELECT Orders.OrderID, Customers.FirstName, SUM(Albums.Price)
                FROM Customers INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID
                INNER JOIN Order_Albums ON Orders.OrderID = Order_Albums.OrderID 
                INNER JOIN Albums ON Order_Albums.AlbumID = Albums.AlbumID 
                WHERE Customers.CustomerID = {user_id} GROUP BY OrderID;"""
    orders = execute_query(connection, query)
    connection.close() 

    return render_template('account-template.html', context={ 
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "favGenre": favGenre,
        "orders": orders 
    })

@app.route('/album', methods=["GET"])
def render_album():
   # album_name = request.args.
    connection = connect() 
    query = f"""SELECT Albums.AlbumID, Albums.AlbumName, Albums.Price, Artists.ArtistName FROM Albums 
    INNER JOIN Album_Artists ON Albums.AlbumID = Album_Artists.AlbumID
    INNER JOIN Artists ON Album_Artists.ArtistID = Artists.ArtistID
    WHERE Albums.AlbumID = {id}
    """
    album_data = execute_query(connection, query)[0]

    query = f"""SELECT Genres.GenreName FROM Genres INNER JOIN Album_Genres ON Genres.GenreID = Album_Genres.GenreID
    INNER JOIN Albums ON Album_Genres.AlbumID = Albums.AlbumID 
    WHERE Albums.AlbumID = {id}"""
    genres = execute_query(connection, query)
    genres = [name[0] for name in genres]

    query = f"""SELECT * FROM Tracks WHERE AlbumID = {id}"""
    tracks = execute_query(connection, query)

    connection.close()
    return render_template('album-template.html', context={ "data": album_data, "genres": genres, "tracks": tracks })

@app.route("/edit-account", methods=["GET", "POST"])
def render_edit_account():
    if request.method == "GET":
        connection = connect()
        user_id = session["user_id"]
        # get user info to display, user favGenreID to get genre name 
        query = f"""select firstName, lastName, email, GenreName from Customers
                    INNER JOIN Genres ON Customers.favGenre = Genres.GenreID
                    where CustomerID = {user_id} """
        user = execute_query(connection, query)
        firstName, lastName, email, favGenre = user[0]
        query = "select GenreID, GenreName from Genres"
        genres = execute_query(connection, query)
        connection.close()
        return render_template("edit-account-template.html", context={
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "favGenre": favGenre,
            "genres": genres
        })
    else:
        try:
            columns = ("FirstName", "LastName", "Email", "FavGenre")
            values = (request.form["firstName"], request.form["lastName"], request.form["email"], int(request.form["favGenre"]))
            model = "Customer"
            update_data(model, columns, values, session["user_id"])
            
            if "error" in session:
                del session["error"]
            
            return redirect("/account")
        except Exception as e: 
            session["error"] = "there was an error updating the customer information"
            return redirect("/edit-account") 


@app.route('/admin')
def render_admin():
    if "admin" not in session or not session["admin"]:
        return render_template("index.html")
    return redirect("/admin/add")

@app.route("/admin/<view>", methods=["GET", "POST"])
def render_admin_add(view):
    if "admin" not in session or not session["admin"]:
        return render_template("index.html")

    if view not in ["add", "edit", "delete", "orders", "search"]:
        view = "add"
   
    return render_template('admin.html', view=view)

@app.route("/admin-search", methods=["GET", "POST"])
def display_search_results():
    if "admin" not in session or not session["admin"]:
        return render_template("index.html")

    album_name = request.form["album-name-input"]
    album_id = request.form["album-id-input"]

    if album_name:
        connection = connect() 
        query = f"""SELECT Albums.AlbumID, Albums.AlbumName, Albums.Price, Artists.ArtistName FROM Albums 
        INNER JOIN Album_Artists ON Albums.AlbumID = Album_Artists.AlbumID
        INNER JOIN Artists ON Album_Artists.ArtistID = Artists.ArtistID
        WHERE Albums.AlbumName = '{album_name}'
        """
        album_data = execute_query(connection, query)[0]
        print(album_data)
        connection.close()
    
    else: 
        connection = connect() 
        query = f"""SELECT Albums.AlbumID, Albums.AlbumName, Albums.Price, Artists.ArtistName FROM Albums 
        INNER JOIN Album_Artists ON Albums.AlbumID = Album_Artists.AlbumID
        INNER JOIN Artists ON Album_Artists.ArtistID = Artists.ArtistID
        WHERE Albums.AlbumID = '{album_id}'
        """
        album_data = execute_query(connection, query)[0]
        print(album_data)
        connection.close()

    return render_template('admin/search-template-results.html', context={ "data": album_data})

@app.route("/admin-album-display-all", methods=["GET", "POST"])
def display_all_albums():
    print("something")
    connection = connect() 
    query = f"""SELECT * FROM Albums 
  
    """
    album_data = execute_query(connection, query)[0]
    print(album_data)
    connection.close()

    return render_template('admin/search-template-results.html', context={ "data": "poop"})

@app.route("/create-account", methods=["GET", "POST"])
def render_create_account():
    if request.method == "POST":
        try:
            values = (
                request.form["firstName"],
                request.form["lastName"],
                request.form["email"],
                int(request.form["favGenre"])
            )
            insert_data("Customers", ["FirstName", "LastName", "Email", "FavGenre"], values)
            return redirect("/")
        except Exception as e:
            print(e)
            return render_template("create-account.html", context={"error": "an error occurred!"})
    else:
        # get list of genres for sidebar menu 
        query = "SELECT GenreName, GenreID FROM Genres"
        connection = connect() 
        genres = execute_query(connection, query)
        connection.close()
        return render_template("create-account.html", context={"genres": genres})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        if request.form["email"] == "admin":
            session["admin"] = True 
            session["logged_in"] = True
            return redirect("/admin/add")
        else:
            # attempt to get user from the database 
            connection = connect()
            email = request.form["email"]
            query = f"select * from customers where email = '{email}'"
            user = execute_query(connection, query)
            connection.close()

            if len(user) == 1:
                session["logged_in"] = True 
                session["user_id"] = user[0][0]
                return redirect("/")
            else:
                return render_template("login.html", context={"error": "user not found"})

@app.route("/logout")
def logout():
    if "logged_in" in session:
        del session["logged_in"]
    if "admin" in session:
        del session["admin"]
    return redirect("/")


# API CALLS 
@app.route("/api/albumsByGenre", methods=["POST"])
def getAlbums():
    data = request.get_json()
    genreID = data["search"]

    connection = connect()
    albums_query = f"""Select Albums.AlbumID, Albums.AlbumName, Artists.ArtistName, 
                Artists.ArtistID, Genres.GenreName FROM Genres
                INNER JOIN Album_Genres ON Genres.GenreID = Album_Genres.GenreID
                INNER JOIN Albums ON Album_Genres.AlbumID = Albums.AlbumID
                INNER JOIN Album_Artists ON Albums.AlbumID = Album_Artists.AlbumID
                INNER JOIN Artists ON Album_Artists.ArtistID = Artists.ArtistID
                WHERE Genres.GenreID = {genreID}"""
    albums = execute_query(connection, albums_query)
 
    connection.close()

    return jsonify(albums)

@app.route("/api/albumsSearch", methods=["POST"])
def searchAlbums():
    data = request.get_json()
    search = data["search"]

    connection = connect()
    albums_query = f"""Select Albums.AlbumID, Albums.AlbumName, Artists.ArtistName, 
                Artists.ArtistID, Genres.GenreName FROM Genres
                INNER JOIN Album_Genres ON Genres.GenreID = Album_Genres.GenreID
                INNER JOIN Albums ON Album_Genres.AlbumID = Albums.AlbumID
                INNER JOIN Album_Artists ON Albums.AlbumID = Album_Artists.AlbumID
                INNER JOIN Artists ON Album_Artists.ArtistID = Artists.ArtistID
                WHERE Genres.GenreName LIKE '%{search}%' OR Artists.ArtistName LIKE '%{search}%'
                OR Albums.AlbumName LIKE '%{search}%'"""
    albums = execute_query(connection, albums_query)
 
    connection.close()

    return jsonify(albums)

if __name__ == "__main__":
    app.run(debug=True)
