from db.connection import connect, execute_query

class Model:  

    def __init__(self, name):
        self.name = name 

    def select(self, columns=("*")):
        query = f"select {columns} from {self.name}"
        connection = connect() 
        return execute_query(connection, query)

    def select_where(self, columns=("*"), where=[]):
        query = f"select {columns} from {self.name}"
        if where:
            query += " AND ".join([f"{x[0]} = {x[1]}" for x in where)
        return execute_query(connection, query)
    
    def query(self, querystring):
        connection = connect()
        return execute_query(connection, querystring)

Genres = Model("Genres")
Albums = Model("Albums")



