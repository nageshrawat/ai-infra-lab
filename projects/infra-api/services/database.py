import psycopg2

def get_connection():
    return psycopg2.connect(
        host="postgres-db",
        database="incidents",
        user="admin",
        password="admin123"
    )