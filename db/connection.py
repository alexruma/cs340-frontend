import mysql.connector 
from db.db_credentials import host, user, password, db  

def connect(host=host, user=user, password=password, db=db): 
    """
    Return connection to database 
    """
    return mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=db
    )

def execute_query(connection, query, params=[]):
    """
    takes a connection, query string, and params to be inserted into query string 
    returns result of query 
    """
    if connection is None:
        print("no connection")
        return 

    if query is None or len(query.strip()) == 0:
        print("query is empty")
        return 

    print(f"Executing {query} with params {params}")

    cursor = connection.cursor(buffered=True) 
    query_params = () 

    for param in params:
        query_params = query_params + (param,)

    # must add data to sanitize query 
    cursor.execute(query, query_params)

    data = cursor.fetchall()
    cursor.close()
    connection.close() 
    return data 


     

