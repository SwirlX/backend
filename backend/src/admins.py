from json import loads
import hashlib
import sqlite3
import utils
import jwt
import error
import data
import auth_helper

def user_is_admin(user_id, db_conn, db_cursor):
    """
    Check if a user is admin

    Parameters:
        user_id: The user's id
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        bool
    """

    if not utils.user_exists(user_id, db_conn, db_cursor):
        raise error.InputError("User doesn't exist")

    cur = db_cursor.execute('SELECT is_admin FROM users WHERE user_id = :user_id', {'user_id': user_id})
    res = cur.fetchone()
    is_admin = res[0]

    return bool(is_admin)

def make_user_admin(user_id, db_conn, db_cursor):
    """
    Make a user an admin

    Parameters:
        user_id: The user's id
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        Nothing
    """

    if not utils.user_exists(user_id, db_conn, db_cursor):
        raise error.InputError("User not found")
    
    # Check that the user is not already admin by checking the db
    cur = db_cursor.execute('SELECT is_admin FROM users WHERE user_id = :user_id', {'user_id': user_id})
    res = cur.fetchone()
    is_admin = res[0]

    if res is None:
        raise error.InputError("User not found")
    elif is_admin:
        raise error.InputError("User is already admin")

    update_query = "UPDATE users SET is_admin = 1 WHERE user_id = :user_id"
    db_cursor.execute(update_query, {'user_id': user_id})
    db_conn.commit()

def demote_admin(user_id, db_conn, db_cursor):
    """
    Demote user from admin to regular user

    Parameters:
        user_id: The user's id
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        Nothing
    """
    if not utils.user_exists(user_id, db_conn, db_cursor):
        raise error.InputError("User not found")
    
    if not user_is_admin(user_id, db_conn, db_cursor):
        raise error.AdminError("User is already not an admin")
    
    update_query = "UPDATE users SET is_admin = 0 WHERE user_id = :user_id"
    db_cursor.execute(update_query, {'user_id': user_id})
    db_conn.commit()


def promote_another_user_as_admin(current_user_id, user_to_promote_id, db_conn, db_cursor):
    """
    Allows another user to promote another user to admin.
    The promoting user must be an admin

    Parameters:
        current_user_id: The current user's id
        user_to_promote_id: The user id of the user to promote
        db_cursor: db cursor

    Returns:
        Nothing
    """

    if not utils.user_exists(user_to_promote_id, db_conn, db_cursor):
        raise error.InputError("User not found")
    
    if not user_is_admin(current_user_id, db_conn, db_cursor):
        raise error.AdminError("Non admin cannot promote user")
    
    make_user_admin(user_to_promote_id, db_conn, db_cursor)

def demote_another_user_as_admin(current_user_id, user_to_demote_id, db_conn, db_cursor):
    """
    Allows another user to demote another user to a regular user.
    The user must be an admin to demote another user

    Parameters:
        current_user_id: The current user's id
        user_to_demote_id: The user id of the user to demote
        db_cursor: db cursor

    Returns:
        Nothing
    """

    if not utils.user_exists(user_to_demote_id, db_conn, db_cursor):
        raise error.InputError("User not found")
    
    if not user_is_admin(current_user_id, db_conn, db_cursor):
        raise error.AdminError("Non admin cannot demote user")
    
    demote_admin(user_to_demote_id, db_conn, db_cursor)