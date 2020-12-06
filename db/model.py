from db.connection import connect, execute_query, execute_non_select_query

class Model:  

    def __init__(self, name= "model"):
        self.name = name 

    def select(self, columns=("*")):
        query = f"select {columns} from {self.name}"
        connection = connect() 
        return execute_query(connection, query)

    # Syntax error with this method. Will look into later.
    # def select_where(self, columns=("*"), where=[]):
    #     query = f"select {columns} from {self.name}"
    #     if where:
    #         query += " AND ".join([f"{x[0]} = {x[1]}" for x in where)
    #     return execute_query(connection, query)
    
    def query(self, querystring):
        connection = connect()
        return execute_query(connection, querystring)

Genres = Model("Genres")
Albums = Model("Albums")


# Table INSERTs
def add_album(name, artist_id, price, copies_in_stock, year, genre_id, second_artist_id = None, second_genre_id = None):
    """ 
    Adds a new album to the DB with the given parametes.
    """
    connection = connect()
    # Insert album into Albums table.
    query = f"""INSERT INTO Albums (AlbumName, Price, ReleasedYear, CopiesInStock)
    VALUES ('{name}', '{price}', '{year}', '{copies_in_stock}')"""
    execute_non_select_query(connection, query)
    connection.close()

    # Get ID of new album.
    album_id = get_album_id_from_name_year(name, year)
    
    # Insert new row into Album_Genres table.
    add_album_genres(album_id, genre_id)

    # Insert second row into Album_Genres table if needed.
    if second_genre_id and second_genre_id != "None":
        add_album_genres(album_id, second_genre_id)

     # Insert new row into Album_Artists table.
    add_album_artists(album_id, artist_id)

    # Insert second row into Album_Artists table if needed.
    if second_artist_id:
        add_album_artists(album_id, second_artist_id)
        print("second "+str(second_artist_id))



def add_artist(name, genre_id = None):
    """ 
    Adds a new artist to the DB with the given name, and if genre is provided, will also add row to Artist_Genres table.
    """
   
    connection = connect()
    
    query = f"""INSERT INTO Artists (ArtistName)
    VALUES ('{name}')"""

    execute_non_select_query(connection, query)
    connection.close()
  
    # Get the newly generated ArtistID.
    artist_id = get_artist_id_from_name(name)
    
    if genre_id:
        # Update Artist_Genres table.
        add_artist_genres(artist_id, genre_id)
        print("done")


def add_track(name, length, album_id):
    """Adds a new track to DB."""

    connection = connect()
    
    query = f"""INSERT INTO Tracks (TrackName, TrackLength, AlbumID)
    VALUES ('{name}', '{length}', '{album_id}')"""

    execute_non_select_query(connection, query)
    connection.close()


# M:M table INSERTs.
def add_artist_genres(artist_id, genre_id):
    """
     Takes an ArtistID and GenreID and adds a new entry to the artist_genre table
    """
    connection = connect()
    
    query = f"""INSERT INTO Artist_Genres (ArtistID, GenreID)
    VALUES ({artist_id}, {genre_id} )"""

    # Execute query and get int value of ID.
    execute_non_select_query(connection, query)

    connection.close()

def add_album_genres(album_id, genre_id):
    """
     Takes an ArtistID and GenreID and adds a new entry to the Album_Genres table
    """
    connection = connect()
    
    query = f"""INSERT INTO Album_Genres (AlbumID, GenreID)
    VALUES ({album_id}, {genre_id} )"""

    # Execute query and get int value of ID.
    execute_non_select_query(connection, query)
   
    connection.close()

def add_album_artists(album_id, artist_id):
    """
     Takes an ArtistID and AlbumID and adds a new entry to the Album_Genres table
    """
    connection = connect()
    
    query = f"""INSERT INTO Album_Artists (AlbumID, ArtistID)
    VALUES ({album_id}, {artist_id} )"""

    # Execute query and get int value of ID.
    execute_non_select_query(connection, query)
    
    connection.close()


# SELECT queries.
def get_artist_id_from_name(name):
    """
    Takes the name of an artist as parameter and returns the ArtistID
    """
    connection = connect()
    
    query = f""" SELECT Artists.ArtistID FROM Artists WHERE Artists.ArtistName = '{name}'"""
    artist_id = execute_query(connection, query)
    
    connection.close()
    
    # Trim ID if it exists to return just int vlaue.
    if artist_id:
        artist_id = artist_id[0][0]
    
    return artist_id

def get_album_id_from_name(name):
    """
    Takes the name of an artist as parameter and returns the ArtistID
    """
    connection = connect()
    
    query = f""" SELECT Albums.AlbumID FROM Albums WHERE Albums.AlbumName = '{name}'"""
    album_id = execute_query(connection, query)
    
    connection.close()
    
    # Trim ID if it exists to return just int vlaue.
    if album_id:
        album_id = album_id[0][0]
    
    return album_id

def get_genre_id_from_name(name):
    """
    Takes the name of an genre as parameter and returns the GenreID.
    """
    connection = connect()
    query = f""" SELECT Genres.GenreID FROM Genres WHERE Genres.GenreName '{name}'"""
   
    # Execute query and get int value of ID.
    genre_id = execute_query(connection, query)[0][0]
    
    connection.close()
    
    return genre_id

def get_album_id_from_name_year(name, year):
    """
    Takes the name and release year of an album as parameter and returns the AlbumID.
    """
    connection = connect()
    query = f""" SELECT Albums.AlbumID FROM Albums WHERE Albums.AlbumName = '{name}' AND Albums.ReleasedYear = '{year}'"""
   
    # Execute query and get int value of ID.
    album_id = execute_query(connection, query)[0][0]
    
    connection.close()
    
    return album_id

def get_all_genres():
    """
    returns list of tuple with genre name and id 
    """
    connection = connect() 
    query = "SELECT GenreID, GenreName FROM Genres";
    genres = execute_query(connection, query)
    
    connection.close()
    
    return genres 

def get_all_artists():
    """
    returns list of tuple with artist name and id 
    """
    connection = connect() 
    query = "SELECT ArtistID, ArtistName FROM Artists"
    artists = execute_query(connection, query)
    
    connection.close()
    
    return artists

def get_all_albums():
    """
    returns list of tuple with album name and id.
    """
    
    connection = connect() 
    query = "SELECT AlbumID, AlbumName FROM Albums"
    albums = execute_query(connection, query)
    
    connection.close()
    
    return albums

def get_all_artists_with_genre():
    """
    Returns all artist names and IDs along with genres associated with each artist, displayed in ascending order by artist name.
    """
    connection = connect() 
    query = f"""SELECT Artists.ArtistName, Artists.ArtistID, Genres.GenreName FROM Artists
        LEFT JOIN Artist_Genres ON Artist_Genres.ArtistID = Artists.ArtistID
        LEFT JOIN Genres ON Genres.GenreID = Artist_Genres.GenreID
        ORDER BY `Artists`.`ArtistName` ASC
        """
    artist_data = execute_query(connection, query)
    
    connection.close()
    
    return artist_data


def get_customer_from_id_or_name(id=None,name=None):
    connection = connect()
    if id:
      query =  f""" SELECT * FROM Customers WHERE CustomerId = '{id}'
        """
    else:
        query = f""" SELECT * FROM Customers WHERE FirstName LIKE '{name}%' OR LastName LIKE '%{name}%'
        """

    try:
        customer_info = execute_query(connection, query)
    except Exception:
        customer_info = ()
    
    connection.close()
    
    return customer_info

def get_album_from_id_or_name(id=None,name=None):
    connection = connect()
    query = f"""SELECT Albums.AlbumID, Albums.AlbumName, Albums.Price, Genres.GenreID, Artists.ArtistID,
            Albums.ReleasedYear, Albums.CopiesInStock FROM Albums 
            LEFT JOIN Album_Artists ON Albums.AlbumID = Album_Artists.AlbumID
            LEFT JOIN Artists ON Artists.ArtistID = Album_Artists.ArtistID
            LEFT JOIN Album_Genres ON Albums.AlbumID = Album_Genres.AlbumID
            LEFT JOIN Genres ON Album_Genres.GenreID = Genres.GenreID"""
    if id:
        query += f" WHERE Albums.AlbumID = {id}"
    else:
        query += f" WHERE Albums.AlbumName LIKE '%{name}%'"

    try:
        album_info = execute_query(connection, query)
    except Exception:
        album_info = ()
    
    #Get track info.
    if album_info != []:
        album_id = album_info[0][0]

        track_query = f"""SELECT Tracks.TrackName, Tracks.TrackLength FROM Tracks WHERE Tracks.AlbumID = {album_id}"""
    
        try:
            tracks = execute_query(connection, track_query)
        except Exception:
            tracks = ()
        print(tracks)
    
    connection.close()
    
    return album_info

# M:M table SELECT Queries:
def get_all_album_artists():
     connection = connect()
     
     query = f""" SELECT * FROM Album_Artists"""
     table_info = execute_query(connection, query)
     
     connection.close()
     
     return table_info


def get_all_album_genres():
     connection = connect()
     
     query = f""" SELECT * FROM Album_Genres"""
     table_info = execute_query(connection, query)
     
     connection.close()
     
     return table_info


def get_all_artist_genres():
     connection = connect()
     
     query = f""" SELECT * FROM Artist_Genres"""
     table_info = execute_query(connection, query)
     
     connection.close()
     
     return table_info
    


# DELETE queries:

def delete_album_by_id(id):
    """ Deletes album with specified ID from Albums table, Album_Artists table and Album_Genres table."""
    connection = connect()
    
    # Delete from Albums table.
    query = f"""DELETE FROM Albums WHERE Albums.AlbumID = {id}"""
    execute_non_select_query(connection, query)

    # Delete from Album_Artists.
    query = f"""DELETE FROM Album_Artists WHERE Album_Artists.AlbumID = {id}"""
    execute_non_select_query(connection, query)

    # Delete from Album_Genres.
    query = f"""DELETE FROM Album_Genres WHERE Album_Genres.AlbumID = {id}"""
    execute_non_select_query(connection, query)

    connection.close()


def delete_customer_by_id(id):
    """ Deletescustomer with specified ID from Customers table."""
    connection = connect()
    
    # Delete from Albums table.
    query = f"""DELETE FROM Customers WHERE Customers.CustomerID = {id}"""
    execute_non_select_query(connection, query)


def delete_artist_by_id(id):
    """ Deletes artist with specified ID from Artists table, Album_Artists table and Artist_Genres table."""
    connection = connect()
    
    # Delete from Albums table.
    query = f"""DELETE FROM Artists WHERE Artists.ArtistID = {id}"""
    execute_non_select_query(connection, query)

    # Delete from Album_Artists.
    query = f"""DELETE FROM Album_Artists WHERE Album_Artists.ArtistID = {id}"""
    execute_non_select_query(connection, query)

    # Delete from Album_Genres.
    query = f"""DELETE FROM Artist_Genres WHERE Artist_Genres.ArtistID = {id}"""
    execute_non_select_query(connection, query)

    connection.close()

# M:M table DELETE queries:
def delete_album_artists_by_id(id):
    """ Deletes Album_Artists row with specified row ID."""
    connection = connect()
    
    query = f"""DELETE FROM Album_Artists WHERE Album_Artists.RowID = {id}"""
    execute_non_select_query(connection, query)

    connection.close()


def delete_album_genres_by_id(id):
    """ Deletes Album_Genres row with specified row ID."""
    connection = connect()
    
    query = f"""DELETE FROM Album_Genres WHERE Album_Genres.RowID = {id}"""
    execute_non_select_query(connection, query)

    connection.close()


def delete_artist_genres_by_id(id):
    """ Deletes Artist_Genres row with specified row ID."""
    connection = connect()
    
    query = f"""DELETE FROM Artist_Genres WHERE Artist_Genres.RowID = {id}"""
    execute_non_select_query(connection, query)

    connection.close()


def update(tableName, fields, values, rowID):
    query = f"UPDATE {tableName} set "
    for i in range(len(fields)):
        if i < len(fields) - 1:
            query += f"{fields[i]} = '{values[i]}', "
        else:
            query += f"{fields[i]} = '{values[i]}' "
    query += f" WHERE {tableName[:-1]}ID = {rowID}"
    try:
        connection = connect() 
        execute_non_select_query(connection, query)
        connection.close() 
        return "success"
    except Exception as e:
        print(e)
        return "fail"

def update_multiple(fk, values, table, parameters):
    connection = connect()
    query1 = f"DELETE FROM Album_Artists WHERE AlbumID = {fk}"
    execute_non_select_query(connection, query1) 

    update_values = ",".join([str((int(fk), int(valueID))) for valueID in values])
    
    fields = ",".join(parameters)
    query2 = f"Insert Into {table} ({fields}) values {update_values}"
    execute_non_select_query(connection, query2)
    connection.close() 

