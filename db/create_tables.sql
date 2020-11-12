CREATE TABLE IF NOT EXISTS Genres(
    GenreID INT NOT NULL AUTO_INCREMENT,
    GenreName VARCHAR(255)	NOT NULL,
    PRIMARY KEY (GenreID),
    UNIQUE (GenreName),
    UNIQUE (GenreID)
);


CREATE TABLE IF NOT EXISTS Customers(
    CustomerID INT NOT NULL AUTO_INCREMENT,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    FavGenre INT,
    PRIMARY KEY (CustomerID),
    FOREIGN KEY (FavGenre) REFERENCES Genres(GenreID) ON DELETE CASCADE,
    UNIQUE (Email)
);

CREATE TABLE IF NOT EXISTS Albums(
    AlbumID INT NOT NULL AUTO_INCREMENT,
    AlbumName VARCHAR(255)	NOT NULL,
    Price INT NOT NULL,
    ReleasedYear INT NOT NULL,
    CopiesInStock INT DEFAULT 100,
    PRIMARY KEY(AlbumID),
    UNIQUE(AlbumID)
);
    
    
CREATE TABLE IF NOT EXISTS Orders(
    	OrderID INT NOT NULL AUTO_INCREMENT PRIMARY KEY UNIQUE,
    	Customer INT NOT NULL,
        CreatedOn DATE DEFAULT "2020-01-01",
        UpdatedOn DATE DEFAULT "2020-01-01",
    	FOREIGN KEY (Customer) REFERENCES Customers (CustomerID) ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS Order_Albums (
   	RowID INT NOT NULL AUTO_INCREMENT,
	OrderID INT	NOT NULL,
    AlbumID INT NOT NULL,
    PRIMARY KEY(RowID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID) ON DELETE CASCADE,
    UNIQUE(RowID)
);

CREATE TABLE IF NOT EXISTS Tracks(
	TrackID INT	AUTO_INCREMENT	NOT NULL,
	TrackName VARCHAR(255)	NOT NULL,
	TrackLength INT	NOT NULL,
	PRIMARY KEY(TrackID),
	UNIQUE (TrackID)
);

CREATE TABLE IF NOT EXISTS Artists(
	ArtistID INT AUTO_INCREMENT	NOT NULL,
	ArtistName VARCHAR(255)	NOT NULL,
	PRIMARY KEY(ArtistID),
	UNIQUE (ArtistID)
);

CREATE TABLE IF NOT EXISTS Artist_Genres(
   	RowID INT NOT NULL AUTO_INCREMENT,
	ArtistID INT NOT NULL,
    GenreID INT NOT NULL,
    PRIMARY KEY(RowID),
    FOREIGN KEY(ArtistID) REFERENCES Artists(ArtistID) ON DELETE CASCADE,
    FOREIGN KEY(GenreID) REFERENCES Genres(GenreID) ON DELETE CASCADE,
    UNIQUE(RowID)
    );

CREATE TABLE IF NOT EXISTS Album_Genres(
   	RowID INT 	NOT NULL 	AUTO_INCREMENT,
	AlbumID INT	NOT NULL,
    GenreID INT 	NOT NULL,
    PRIMARY KEY(RowID),
    FOREIGN KEY(AlbumID) REFERENCES Albums (AlbumID) ON DELETE CASCADE,
    FOREIGN KEY(GenreID) REFERENCES Genres(GenreID) ON DELETE CASCADE,
    UNIQUE(RowID)
);

CREATE TABLE IF NOT EXISTS Album_Artists (
    RowID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    AlbumID INT NOT NULL,
    ArtistID INT NOT NULL,
    FOREIGN KEY (AlbumID) REFERENCES Albums (AlbumID) ON DELETE CASCADE,
    FOREIGN KEY (ArtistID) REFERENCES Artists (ArtistID) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Customers_Genres(
   	RowID INT NOT NULL AUTO_INCREMENT,
	CustomerID INT	NOT NULL,
    GenreID INT NOT NULL,
    PRIMARY KEY (RowID),
    FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (GenreID) REFERENCES Genres (GenreID) ON DELETE CASCADE,
    UNIQUE(RowID)
);


--Insert Statments

INSERT INTO Genres (GenreName) VALUES 
("Hip Hop"),
("Rock"),               
("Pop"),                
("Jazz"),               
("Punk"),               
("Post-Punk"),          
("Funk"),               
("Alternative"),         
("Indie"),               
("Folk"),               
("EDM"),                 
("R&B");                 

INSERT INTO Customers(FirstName, LastName, Email, FavGenre) VALUES 
("Alex", "Ruma", "rumaa@oregonstate.edu", 1),     
("Pete", "Pistachio", "pp@test.edu", 4),          
("Joey", "Juxtaposition", "jj@test.edu", 6);      

INSERT INTO Artists (ArtistName) VALUES 
("A Tribe Called Quest"),
("Radiohead"),
("Modest Mouse"),
("Vulfpeck"),
("Kendrick Lamar"),
("The Smiths"),
("Built to Spill"),
("Gucci Mane"),
("Bill Withers"),
("Outkast"),
("Ariana Grande"),
("Neil Young"),
("Jay-Z"),
("Linkin Park");

INSERT INTO Artist_Genres (ArtistID, GenreID) VALUES 
(1, 1),
(1, 4),
(2, 2),
(2, 8),
(3, 9),
(4, 7),
(5, 1),
(6, 6),
(6, 8),
(6, 9),
(7, 9),
(7, 8),
(8, 1),
(9, 12),
(10, 1),
(11, 3),
(11, 12),
(12, 10),
(13, 1),
(14, 2);

INSERT INTO Albums (AlbumName, Price, ReleasedYear) VALUES 
("the low end theory", 1299, 1990),
("midnight marauders", 1299, 1990),
("pablo honey", 1299, 1993),
("the bends", 1299, 1995),
("this is a long drive for someone with nothing to think about", 1299, 1996),
("the lonesome crowded west", 1299, 1997),
("the thrill of the arts", 1299, 2015),
("the beautiful game", 1299, 2016),
("untitled unmastered",  1299, 2016),
("collision course", 1299, 2004);

INSERT INTO Album_Genres (AlbumID, GenreID) VALUES 
(1, 1),
(1, 4),
(2, 1),
(3, 8),
(4, 8),
(5, 9),
(6, 9),
(7, 7),
(8, 1),
(9, 1),
(9, 2);

INSERT INTO Album_Artists (AlbumID, ArtistID) VALUES 
(1, 1),
(2, 1),
(3, 2),
(4, 2),
(5, 3),
(6, 3),
(7, 4),
(8, 4),
(9, 5),
(10, 13),
(10, 14);

INSERT INTO Orders (Customer, CreatedOn) VALUES 
(1, "2020-10-20"),
(1, "2020-10-30"),
(1, "2020-11-10"),
(2, "2020-11-01"),
(3, "2020-11-10");

INSERT INTO Order_Albums (OrderID, AlbumID) VALUES 
(1, 1),
(1, 2),
(1, 3),
(2, 4),
(2, 5),
(3, 6),
(3, 7),
(4, 1),
(5, 10);