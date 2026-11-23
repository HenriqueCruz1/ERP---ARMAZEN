import psycopg

def conectar():
    return psycopg.connect(
        dbname="erp",
        user="postgres",
        password="######",
        host="localhost"
    )