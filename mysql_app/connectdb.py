import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="mysql.iotserver.uz",
        user="caruser",
        password="CarDBuser123",
        database="caruser",
        port=3306
    )
    return connection
