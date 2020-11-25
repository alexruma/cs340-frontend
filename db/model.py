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
def add_album(name, artist_id, price, copies_in_stock, year, genre_id):
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

     # Insert new row into Album_Genres table.
    add_album_artists(album_id, artist_id)


def add_artist(name, genre_id = None):
    """ 
    Adds a new artist to the DB with the given name.
    """
   
    connection = connect()
    query = f"""INSERT INTO Artists (ArtistName)
    VALUES ('{name}')"""

    execute_non_select_query(connection, query)
    connection.close()
  
    # Get the newly generated ArtistID.
    artist_id = get_artist_id_from_name(name)
    print(artist_id)
    
    if genre_id:
        # Update Artist_Genres table.
        add_artist_genres(artist_id, genre_id)
        print("done")


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


def get_artist_id_from_name(name):
    """
    Takes the name of an artist as parameter and returns the ArtistID
    """
    connection = connect()
    query = f""" SELECT Artists.ArtistID FROM Artists WHERE Artists.ArtistName = '{name}'"""
    artist_id = execute_query(connection, query)
    connection.close()
    
    # Trim ID it it exists to return just int vlaue.
    if artist_id:
        artist_id = artist_id[0][0]
    
    return artist_id

def get_genre_id_from_name(name):
    """
    Takes the name of an genre as parameter and returns the GenreID.
    """
    connection = connect()
    query = f""" SELECT Genres.GenreID FROM Genres WHERE Genres.GenreName = '{name}'"""
   
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



