import mysql.connector

def connect_to_database():
    conn = mysql.connector.connect(
        host="speedspot-db-do-user-16519834-0.c.db.ondigitalocean.com",
        port="25060",
        user="doadmin",
        password="AVNS_DCLwHjp1kyF7kj3AsHv",
        database="Speedspot"
    )
    return conn
