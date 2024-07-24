import sqlite3
import utils

def db_setup():

    con = sqlite3.connect(utils.DB_PATH)
    cur = con.cursor()

    return con, cur

def db_close(con: sqlite3.Connection):
    con.close()

def example_db_query(cur: sqlite3.Cursor):
    query = "SELECT * FROM name_basics LIMIT 10"
    cur.execute(query)

    movies = cur.fetchall()

    for tup in movies:
        print(tup)
    

if __name__ == "__main__":
    con, cur = db_setup()
    example_db_query(cur)
    db_close(con)
    