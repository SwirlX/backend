import sqlite3
import error

def get_user_details(user_id, db_conn, db_cursor):
    """
    Get all the details of a user

    Parameters:
        user_id: The users id
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        Dict: {first_name, last_name, email, dob, token, is_admin, is_child}        
    """
    res = db_cursor.execute("SELECT first_name, last_name, email, dob, token, is_admin, is_child FROM users WHERE user_id =?", (user_id,))
    rows = res.fetchone()

    if rows is None:
        raise error.InputError("User not found")
    
    return {
        "first_name": rows[0],
        "last_name": rows[1],
        "email": rows[2],
        "dob": rows[3],
        "token": rows[4],
        "is_admin": rows[5],
        "is_child": rows[6]
    }

def get_all_users(db_conn, db_cursor):
    """
    Gets all users on the platform

    Parameters:
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        List: [{first_name, last_name, email, dob, token, is_admin, is_child}]
    """
    res = db_cursor.execute("SELECT user_id, first_name, last_name, email, dob, token, is_admin, is_child FROM users")
    rows = res.fetchall()

    list_of_users = []
    for row in rows:
        user_dict = {
            "user_id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "email": row[3],
            "dob": row[4],
            "token": row[5],
            "is_admin": row[6],
            "is_child": row[7]
        }
        list_of_users.append(user_dict)

    return list_of_users

