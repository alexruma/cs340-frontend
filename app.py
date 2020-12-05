import os

from flask import Flask, render_template, request, session, redirect, jsonify, url_for, flash
import requests
from db.connection import connect, execute_query, insert_data, update_data
from db.model import * 

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
                where Customers.CustomerID = {user_id} """
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

@app.route('/album/<int:id>', methods=["GET"])
def render_album(id):
   # album_name = request.args.
    connection = connect() 
    query = f"""SELECT Albums.AlbumID, Albums.AlbumName, Albums.Price, Artists.ArtistName FROM Albums 
    INNER JOIN Album_Artists ON Albums.AlbumID = Album_Artists.AlbumID
    INNER JOIN Artists ON Album_Artists.ArtistID = Artists.ArtistID
    WHERE Albums.AlbumID = {id}
    """
    album_data = execute_query(connection, query)

    # return a 404 if an album wasn't found 
    if not album_data:
        return render_template("404-template.html")
    
    album_data = album_data[0]

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

    if view not in ["add", "edit", "delete", "orders", "search", "search-results"]:
        view = "add"
    
    artists = get_all_artists()
    genres = get_all_genres()
    albums = get_all_albums()
    
    return render_template('admin.html', view = view, artists = artists, genres = genres, albums = albums)


##SEARCH PAGE ROUTING 

# Customer search for albums by name or ID.
@app.route("/admin-customer-search", methods=["GET", "POST"])
def display_customer_search_results():
    if "admin" not in session or not session["admin"]:
        return render_template("index.html")
   
    customer_name = request.form["customer-name-input"]
    customer_id = request.form["customer-id-input"]
    
    # Search by customer name.
    if customer_name:
       customer_data = get_customer_from_id_or_name(None, customer_name)
    
    # Search by customer ID.
    else:
        customer_data = get_customer_from_id_or_name(customer_id)
    
    return render_template('admin/search-template-results.html', album_data = [], customer_data = customer_data)


# Admin display all customers.
@app.route("/admin-customer-display-all", methods=["GET", "POST"])
def display_all_customers():

    connection = connect() 
    query = f""" SELECT * FROM Customers"""
    customer_data = execute_query(connection, query)
    connection.close()

    return render_template('admin/search-template-results.html', album_data = [], customer_data = customer_data)


# Adimn search for albums by name or ID.
@app.route("/admin-search", methods=["GET", "POST"])
def display_search_results():
    if "admin" not in session or not session["admin"]:
        return render_template("index.html")

    album_name = request.form["album-name-input"]
    album_id = request.form["album-id-input"]
    
    # Search by album name.
    if album_name:
        album_data = get_album_from_id_or_name(None,album_name)
    
    # Search by ID.
    else: 
       album_data = get_album_from_id_or_name(album_id)

    #return redirect("/admin/search-results")
    return render_template('admin/search-template-results.html', album_data = album_data)


# Admin display all albums.
@app.route("/admin-album-display-all", methods=["GET", "POST"])
def display_all_albums():

    connection = connect() 
    query = f"""SELECT Albums.AlbumID, Albums.AlbumName, Albums.Price, Artists.ArtistName, Albums.CopiesInStock, Albums.ReleasedYear FROM Albums 
        INNER JOIN Album_Artists ON Albums.AlbumID = Album_Artists.AlbumID
        INNER JOIN Artists ON Album_Artists.ArtistID = Artists.ArtistID
        """
    album_data = execute_query(connection, query)
    connection.close()
    
    # return redirect("/admin/search-results")
    return render_template('admin/search-template-results.html', album_data = album_data)


# Admin display all artists.
@app.route("/admin-artist-display-all", methods=["GET", "POST"])
def display_all_artists():

    artist_data = get_all_artists_with_genre()
    
    # return redirect("/admin/search-results")
    return render_template('admin/search-template-results.html', artist_data = artist_data)


# Admin display all Artist_Albums
@app.route("/admin-album_artists-display-all", methods=["GET", "POST"])
def display_all_album_artists():
    table_data = get_all_album_artists()

    return render_template('admin/search-template-results.html', data = table_data)


# Admin display all Album_Genres
@app.route("/admin-album_genres-display-all", methods=["GET", "POST"])
def display_all_album_genres():
    album_genres_data = get_all_album_genres()

    return render_template('admin/search-template-results.html', album_genres_data =  album_genres_data)


##ADMIN ADD PAGE ROUTING

# Add album to DB.
@app.route("/add-album", methods = ["POST"])
def admin_add_album():
   
    # Get POST request data'
    album_name = request.form['album-name']
    artist_name = request.form['artist-name']
    second_artist_name = request.form['second-artist-name']
    price = request.form['price']
    copies_in_stock = request.form['copiesInStock']
    release_year = request.form['year']
    genre_id = request.form['genre']
    second_genre_id = request.form['second-genre']
   
    # Process to add album with multiple artists.
    if second_artist_name:
        # Verify that artist exists.
        artist_id = get_artist_id_from_name(artist_name)

        # Add arist if does not exist.
        if not artist_id:
            add_artist(artist_name, genre_id)
            artist_id = get_artist_id_from_name(artist_name)
        
         # Verify that second artist exists.
        second_artist_id = get_artist_id_from_name(second_artist_name)

        # Add second arist if does not exist.
        if not second_artist_id:
            add_artist(second_artist_name, genre_id)
            second_artist_id = get_artist_id_from_name(artist_name)
        
        # Add album
        add_album(album_name, artist_id, price, copies_in_stock, release_year, genre_id, second_artist_id, second_genre_id)
    

    # Process to add album with single artist.
    else:
        # Verify that artist exists.
        artist_id = get_artist_id_from_name(artist_name)

        # Add arist if does not exist.
        if not artist_id:
            add_artist(artist_name, genre_id)
            artist_id = get_artist_id_from_name(artist_name)
        
        # Add album
        add_album(album_name, artist_id, price, copies_in_stock, release_year, genre_id, None, second_genre_id)
    
    return redirect("/admin/add")


# Add artist to DB.
@app.route("/add-artist", methods = ["POST"])
def admin_add_artist():
    artist_name = request.form['artist-name']
    
    add_artist(artist_name)
    
    return redirect("/admin/add")


# Add track to DB.
@app.route("/add-track", methods = ["POST"])
def admin_add_track():
    track_name = request.form['track-name']
    length = request.form['track-length']
    album_id = request.form['album-id']
    
    add_track(track_name, length, album_id)
    
    return redirect("/admin/add")


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


##ADMIN DELETE ROUTING
# Delete Album.
@app.route("/delete-album", methods=["GET", "POST"])
def admin_delete_album():
    album_id = request.form['delete-id']
    delete_album_by_id(album_id)

    flash('Album ' + str(album_id) + ' Removed From Database')
    return redirect("/admin-album-display-all")


# Delete Customer.
@app.route("/delete-customer", methods=["GET", "POST"])
def admin_delete_customer():
    customer_id = request.form['delete-id']
    delete_customer_by_id(customer_id)

    flash('Customer ' + str(customer_id) + ' Removed From Database')
    return redirect("/admin-customer-display-all")


# Delete Artist.
@app.route("/delete-artist", methods=["GET", "POST"])
def admin_delete_artist():
    artist_id = request.form['delete-id']

    delete_artist_by_id(artist_id)
    
    flash('Artist ' + str(artist_id) + ' Removed From Database')
    return redirect("/admin-artist-display-all")


# Delete Album_Artists.
@app.route("/delete-album-artists", methods=["GET", "POST"])
def admin_delete_album_artists():
    row_id = request.form['delete-id']

    delete_album_artists_by_id(row_id)
    
    flash('Row ' + str(row_id) + ' Removed From Database')
    return redirect("/admin-album_artist-display-all")

# Delete Album_Genres.
@app.route("/delete-album-genres", methods=["GET", "POST"])
def admin_delete_album_genres():
    row_id = request.form['delete-id']

    delete_album_genres_by_id(row_id)
    
    flash('Row ' + str(row_id) + ' Removed From Database')
    return redirect("/admin-album_genres-display-all")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        if request.form["email"] == "admin":
            session["admin"] = True 
            session["logged_in"] = True
            session["user_id"] = 1 # admin user is Alex Ruma
            return redirect("/admin/add")
        else:
            # attempt to get user from the database 
            connection = connect()
            email = request.form["email"]
            query = f"select * from Customers where email = '{email}'"
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

@app.route("/api/getAlbumDetails", methods=["POST"])
def getAlbumDetails():
    data = request.get_json()
    albumID = data["albumID"]
    albumName = data["albumName"]
    album = get_album_from_id_or_name(id=albumID, name = albumName)
    genres = [album[0][3]]
    artists = [album[0][4]]
    if len(album) > 1:
        for result in album:
            if result[3] not in genres:
                genres.append(result[3])
            if result[4] not in artists:
                artists.append(result[4])
    return jsonify(album[0], artists, genres)

@app.route("/api/updateAlbum", methods=["POST"])
def updateAlbum():
    data = request.get_json() 
    fields = ["AlbumName", "Price", "ReleasedYear", "CopiesInStock"]
    values = [data["albumName"], data["price"], data["ReleasedYear"], data["CopiesInStock"]]
    status = update("Albums", fields, values, data["albumID"])
    return jsonify({ "status" : status })

@app.route("/api/getArtist", methods=["POST"])
def getArtist():
    data = request.get_json()
    print(data)
    artist = get_artist_id_from_name(data["artistName"])
    return jsonify(artist)

@app.route("/api/updateArtist", methods=["POST"])
def updateArtist():
    data = request.get_json()
    artistID = data["artistID"]
    artistName = data["artistName"]
    status = update("Artists", ["artistName"], [artistName], artistID)
    return jsonify(status)

@app.route("/api/updateGenre", methods=["POST"])
def updateGenre():
    data = request.get_json()
    oldGenre = data["oldGenre"]
    newGenre = data["newGenre"]
    genreID = get_genre_id_from_name(oldGenre) 
    status = update("Genres", ["genreName"], [newGenre], genreID)
    print(status)
    return jsonify(status)

@app.route("/api/createOrder", methods=["POST"])
def createOrder():
    if not "logged_in" in session or not session["logged_in"]:
        return jsonify({ "status": "fail"})
    
    user_id = session["user_id"]
    data = request.get_json()
    albums = data["albums"]
    status = create_order(user_id, albums)
    return jsonify({ "status": status })


if __name__ == "__main__":
    app.run(debug=True)
