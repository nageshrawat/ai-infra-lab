import psycopg2

conn = psycopg2.connect(
    host="postgres-db",
    database="incidents",
    user="admin",
    password="admin123"
)

print("Database Connected Successfully!")

conn.close()