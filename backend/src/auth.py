import sys
import os
from json import loads
import hashlib
import sqlite3
import jwt
import error
import data
import auth_helper
import kids_friendly_mode
import admins

def register_user(email, password, first_name, last_name, dob, age, db_conn, db_cursor):
    """
    Registers a user in the system

    Parameters:
        email
        password
        first_name
        last_name
        dob: Date of birth
        age: Age of the user
        db_conn: Db connection
        db_cursor: db cursor

    Returns:
        Dict: {user_id, token}        
    """

    for field in [email, password, first_name, last_name, dob]:
        if not field:
            raise error.InputError("Please fill in all fields")

    # Check if user already exists
    get_id_query = "SELECT user_id FROM users WHERE email = :email"
    db_cursor.execute(get_id_query, {"email": email})

    if db_cursor.fetchone():
        raise error.InputError("User already exists")
    
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
 
    sql_params = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password_hashed": password_hashed,
        "dob": dob
    }

    sql_query = "INSERT INTO users (first_name, last_name, email, password, dob, token) VALUES (:first_name, :last_name, :email, :password_hashed, :dob, NULL)"

    try:
        db_cursor.execute(sql_query, sql_params)
        db_conn.commit()
    except sqlite3.IntegrityError as e:
        raise error.InputError(e)

    get_id_query = "SELECT user_id FROM users WHERE email = :email"
    db_cursor.execute(get_id_query, {"email": email})

    user_id = db_cursor.fetchone()[0]

    jwt_token = jwt.encode({'user_id' : user_id}, data.SECRET, algorithm='HS256')
    update_token_sql = "UPDATE users SET token = :token WHERE user_id = :user_id"

    try:
        db_cursor.execute(update_token_sql, {"token": jwt_token, "user_id": user_id})
        db_conn.commit()
    except Exception as e:
        raise Exception(e)
    
    # Process if user `is_child`
    kids_friendly_mode.run_child_user_account_logic(user_id, int(age), db_conn, db_cursor)

    return_user = {}
    return_user['user_id'] = user_id
    return_user['token'] = jwt_token
    return return_user


def register_user_child(email, password, first_name, last_name, dob, age, db_conn, db_cursor):
    """
    Registers a child user in the system

    Parameters:
        email
        password
        first_name
        last_name
        dob: Date of birth
        age: Age of the user
        db_conn: Db connection
        db_cursor: db cursor

    Returns:
        Dict: {user_id, token}        
    """

    for field in [email, password, first_name, last_name, dob]:
        if not field:
            raise error.InputError("Please fill in all fields")

    # Check if user already exists
    get_id_query = "SELECT user_id FROM users WHERE email = :email"
    db_cursor.execute(get_id_query, {"email": email})

    if db_cursor.fetchone():
        raise error.InputError("User already exists")
    
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
 
    sql_params = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password_hashed": password_hashed,
        "dob": dob
    }

    sql_query = "INSERT INTO users (first_name, last_name, email, password, dob, token) VALUES (:first_name, :last_name, :email, :password_hashed, :dob, NULL)"

    try:
        db_cursor.execute(sql_query, sql_params)
        db_conn.commit()
    except sqlite3.IntegrityError as e:
        raise error.InputError(e)

    get_id_query = "SELECT user_id FROM users WHERE email = :email"
    db_cursor.execute(get_id_query, {"email": email})

    user_id = db_cursor.fetchone()[0]


    # Process if user `is_child`
    kids_friendly_mode.run_child_user_account_logic(user_id, int(age), db_conn, db_cursor)

    return_user = {
        'is_success' : True
    }

    return return_user


    
def login_user(email, password, db_conn, db_cursor):
    """
    Take in user details, return whether the login attempt is successful

    Parameters:
        email
        password
        db_conn: Db connection
        db_cursor: db cursor

    Returns:
        Dict: {user_id, token}  
    """ 

    # Hashed password 
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    
    sql_query = "SELECT user_id, email, password, token FROM users WHERE email = :email"
    
    db_cursor.execute(sql_query, {"email": email})
    rows = db_cursor.fetchone()

    if rows == None:
        raise error.InputError("The provided email is not registered")

    returned_user_id = rows[0]
    returned_email = rows[1]
    returned_password = rows[2]
    returned_token = rows[3]

    if returned_password != password_hashed:
        # Incorrect password
        raise error.InputError("Invalid password")
    admin = admins.user_is_admin(str(returned_user_id), db_conn, db_cursor)
    if returned_token != None and not admin:
        raise error.AccessError("User is already logged in")

    jwt_token = jwt.encode({'user_id' : returned_user_id}, data.SECRET, algorithm='HS256')
    update_token_sql = "UPDATE users SET token = :token WHERE user_id = :user_id"

    try:
        db_cursor.execute(update_token_sql, {"token": jwt_token, "user_id": returned_user_id})
        db_conn.commit()
    except Exception as e:
        raise Exception(e)

    return_user = {}
    return_user['user_id'] = returned_user_id
    return_user['token'] = jwt_token
    return return_user

def logout_user(token, db_conn, db_cursor):

    """
    Log a user out of the system

    Parameters:
        token: User's session token
        db_cursor: db cursor

    Returns:
        Dict: {is_success}  
    """ 


    check_user_sql_query = "SELECT user_id FROM users WHERE token = :token"
    db_cursor.execute(check_user_sql_query, {"token": token})


    user_id = db_cursor.fetchone()

    if user_id == None:
        raise error.InputError("Invalid token: user may not be logged in")
    
    user = user_id[0]
    admin = admins.user_is_admin(str(user), db_conn, db_cursor)

    if admin:
        return {"is_success": True}

    logout_sql_query = "UPDATE users SET token = NULL WHERE token = :token"

    try:
        db_cursor.execute(logout_sql_query, {"token": token})
        db_conn.commit()
    except:
        raise error.InputError("Invalid token")
    
    return {"is_success": True}
    
def password_reset_request(email, db_conn, db_cursor):
    '''
    Given a registered email, send a specific code secret code to the email so that 
    when entered in password_reset_reset validates that the person attempting to change 
    the password is the right person.

    Parameters:
        email
        db_cursor: db cursor
        db_con: db connection

    Returns:
        string: reset_code
    '''

    # Check if the email is a registered email address
    sql_query = "SELECT email FROM users WHERE email = :email"
    
    try:
        db_cursor.execute(sql_query, {"email": email})
        db_conn.commit()
    except:
        raise error.InputError("Invalid token")
    
    rows = db_cursor.fetchone()

    # If email address is not registered
    if rows == None:
        raise error.InputError("The provided email is not registered")
    
    # Capture the email address so that the reset code can be sent to email address
    receiver_email = rows[0]
    
    # Generate the reset code
    reset_code = auth_helper.generate_reset_code()
    auth_helper.send_reset_code(receiver_email, reset_code)
    
    # Send the reset_code to the front-end
    return reset_code
    
    
def password_reset_reset(email, new_password, db_conn, db_cursor):
    '''
    Given a valid email, update the old password to the new password.

    Parameters:
        email
        new_password
        db_cursor: db cursor
        db_con: db connection

    Returns:
        Dict: {is_success}
    '''

    new_password_hashed = hashlib.sha256(new_password.encode()).hexdigest()
    
    # Update the password to the new password that is passed in
    update_password_sql = "UPDATE users SET password = :new_password WHERE email = :email"
    
    try:
        db_cursor.execute(update_password_sql, {"email": email, "new_password": new_password_hashed})
        db_conn.commit()
    except:
        # TO DO: find a better informative message, technically speaking this should not fail
        raise error.InputError("Invalid email")
        
    return {"is_success": True}