import utils
import error
import users
from datetime import datetime, timedelta


def is_user_child(user_id, db_conn, db_cursor):
    """
    Check if a user account is a child account

    Parameters:
        user_id (int): The user ID of the user
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        bool
    """
    if user_id is None:
        return False

    if not utils.user_exists(user_id, db_conn, db_cursor):
        return False # User is probably not signed in

    query = "SELECT is_child FROM users WHERE user_id = :user_id"
    res = db_cursor.execute(query, {"user_id": user_id})
    is_child_user = res.fetchone()[0]

    return bool(is_child_user)

def make_user_child_account(user_id, db_conn, db_cursor):
    """
    Make a user account a child account

    Parameters:
        user_id (int): The user ID of the user
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        None
    """

    if is_user_child(user_id, db_conn, db_cursor):
        raise error.PermissionError("Cannot make child account: Account is already child account")
    
    query = "UPDATE users SET is_child = 1 WHERE user_id = :user_id"
    db_cursor.execute(query, {"user_id": user_id})
    db_conn.commit()

def make_child_account_regular_account(user_id, db_conn, db_cursor):
    """
    Make a child account a regular account

    Parameters:
        user_id (int): The user ID of the user
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        None
    """

    if not is_user_child(user_id, db_conn, db_cursor):
        raise error.PermissionError("Cannot convert to regular account: Account is already a regular account")
    
    query = "UPDATE users SET is_child = 0 WHERE user_id = :user_id"
    db_cursor.execute(query, {"user_id": user_id})
    db_conn.commit()

def run_child_user_account_logic(user_id, age, db_conn, db_cursor):
    """
    Runs the logic for creating a child account based on age

    Parameters:
        user_id (int): The user ID of the user
        aeg: The age of user
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        None
    """

    if age < 18:
        make_user_child_account(user_id, db_conn, db_cursor)

