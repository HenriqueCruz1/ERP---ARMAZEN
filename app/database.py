import psycopg

def conectar():
    return psycopg.connect(
        dbname="erp",
        user="postgres",
        password="Mh1*4*7*",
        host="localhost"
    )