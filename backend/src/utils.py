import os
import error
import auth
import admins
import sqlite3


DB_PATH = os.path.abspath("../db/mydb.db")

def user_exists(user_id, db_conn, db_cursor):
    """
    Check if a user exists

    Parameters:
        user_id: The user's id
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        bool
    """

    db_cursor.execute('SELECT user_id FROM users WHERE user_id =?', (user_id,))
    check_user_id = db_cursor.fetchone()

    return check_user_id is not None

# Check if movies exists
def movie_exists(tconst, db_conn, db_cursor):
    """
    Check if a movie exists in the db

    Parameters:
        tconst: The movie's tconst id
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        bool
    """
    db_cursor.execute('SELECT tconst FROM title_basics WHERE tconst =?', (tconst,))
    tconst = db_cursor.fetchone()

    return tconst is not None

def create_default_admin():
    """
    Create the default admin user

    Parameters:
        
    Returns:
        None
    """

    db_conn = sqlite3.connect(DB_PATH)
    db_cursor = db_conn.cursor()
    # Check if admin user already exists
    cur = db_cursor.execute('SELECT user_id FROM users WHERE email = "admin@admin.com"')
    res = cur.fetchone()

    if res is not None:
        return

    admin_user = auth.register_user('admin@admin.com', 'admin', 'admin_first_name', 'admin_last_name', '01/01/1990', '100', db_conn, db_cursor)
    admin_user_id = admin_user["user_id"]
    admins.make_user_admin(admin_user_id, db_conn, db_cursor)

if __name__ == "__main__":
    create_default_admin()
