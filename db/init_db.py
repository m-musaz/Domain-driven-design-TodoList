import psycopg2

connection = psycopg2.connect(
    "postgresql://postgres:25100107@localhost:5432/postgres")

cursor = connection.cursor()

with open("../db/initialize-db.sql") as sql_init:
    sql = sql_init.read()

    cursor.execute(sql)

    connection.commit()

    print("Project DB initialized")
