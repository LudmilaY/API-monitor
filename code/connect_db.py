import psycopg2

def connect_db():
    return psycopg2.connect(
        host="localhost",
        dbname="apiusinas",
        user="postgres",
        password="postgres"
    )
