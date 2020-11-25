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
    return data

def execute_non_select_query(connection, query, params=()):
    """
    Same as as execute_query() but does not return anything.
    Takes a connection, query string, and params to be inserted into query string. 
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
    
    # Commit chnge
    connection.commit()
    cursor.close()






def insert_data(table, columns, values):
    connection = connect()
    cursor = connection.cursor()
    columns = ", ".join(columns)
    query = f"Insert into {table} (" + columns + f") values {values}"
    cursor.execute(query)
    connection.commit()
    cursor.close() 
    connection.close()

def update_data(model, columns, values, row):
    if len(columns) != len(values):
        raise ValueError

    connection = connect()
    cursor = connection.cursor() 
    query = f"UPDATE {model}s SET "
    for i in range(len(columns)):
        if type(values[i]) == str:
            query += f"{columns[i]} = '{values[i]}'"
        else:
            query += f"{columns[i]} = {values[i]}"

        if i < len(columns) - 1:
            query += ", "
        else:
            query += " "

    query += f"WHERE {model}ID = {row}"
    cursor.execute(query) 
    connection.commit()
    cursor.close()
    connection.close() 


    


     

