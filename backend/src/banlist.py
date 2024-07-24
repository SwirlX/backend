import sys
import os
import sqlite3
import error
import utils

# list_format - [2,3,4,5]
# db_form - 2,3,4,5

# When adding and removing from the banlist, we will deal with the banlist in
# the python list format referred to as 'list_format'. 
# i.e. [2,3,4,5] where 2,3,4 and 5 are the users on the banlist.

# When storing the banlist it will be stored in the user_banlist as 
# comma separated values referred to as the 'db_form'
# i.e. [2,3,4,5] will be stored as 2,3,4,5 in the 'banlist' column

# Function to convert between python list format to csv format
def convert_banlist_to_db_form(current_banlist):
    """_summary_
    Convert the banlist from a list in python to a CSV format.
    ['2', '3', '4', '5'] -> '2,3,4,5'
    Args:
        current_banlist (list): the banlist that currently exists for the user

    Returns:
        string: csv string form of the banlist
    """
    return ','.join(current_banlist)

# Function to convert between csv format to python list format
def convert_banlist_to_list_form(current_banlist):
    """_summary_
    Convert the banlist from a CSV format to a list in python.
    '2,3,4,5' -> ['2', '3', '4', '5']
    Args:
        current_banlist (string): the banlist that currently exists for the user

    Returns:
        list: list form of the banlist
    """
    list_form = current_banlist.rsplit(',')
    return list_form

# Function to create a banlist if it does not exist
def create_banlist():
    """_summary_

    Returns:
        list: empty banlist
    """
    return []

# Function to add a user to their banlist
def add_user_to_banlist(current_banlist, user_id_to_ban):
    """_summary_
    Adds a user_id_to_ban to the current_banlist that gets passed in.
    Args:
        current_banlist (list): the banlist that currently exists for the user 
        user_id_to_ban (integer): the user_id that is to be added to the current banlist

    Returns:
        current_banlist (list): Returns an updated list 
                                containing the new user that was banned. 
    """
    # Check if the current_banlist does not exist
    if current_banlist == []:
        current_banlist = create_banlist()
        current_banlist.append(str(user_id_to_ban))
        return current_banlist
    
    # Check if the user you are trying to ban is not currently in the list
    # If they are already in the list, raise an error.
    if str(user_id_to_ban) not in current_banlist:
        current_banlist.append(str(user_id_to_ban))
    elif str(user_id_to_ban) in current_banlist:
        raise error.InputError("You are attempting to add a user that is already in your banlist.")
        
    return current_banlist

    
# Function to remove a user from their banlist
def remove_user_from_banlist(current_banlist, user_id_to_remove):
    """_summary_
    Removes the user_id_to_remove from the banlist
    Args:
        current_banlist (list): the banlist that currently exists for the user
        user_id_to_remove (integer): e user_id that is to be removed from the current banlist

    Raises:
        error.InputError: if the banlist is empty
        error.InputError: removing a user that is not in the current banlist

    Returns:
        list: updated version of the banlist with the user removed 
    """
    # Cast the user_id_to_remove to str form
    user_id_to_remove = str(user_id_to_remove)
    
    # Check if the banlist is empty for the current user
    if current_banlist == []:
        raise error.InputError("Banlist does not exist for user")

    # Check if user is in the banlist is in the banlist before removing
    if user_id_to_remove in current_banlist:
        current_banlist.remove(user_id_to_remove)
    elif user_id_to_remove not in current_banlist:
        raise error.InputError("Attempting to remove a user that is not in the banlist")
   
    return current_banlist  

# Function to extract from the banlist
def extract_banlist_from_db(user_id, db_conn, db_cursor):
    """_summary_
    Extracts the banlist from user_banlist table given a specific user_id
    Args:
        user_id (string): user_id of the user whose banlist we want
        db_conn (_type_): connection to the database
        db_cursor (_type_): cursor for the database

    Returns:
        list: the banlist for the given user_id in the python list format
    """
    extract_query_params = {
        "user_id": user_id
    }
    
    extract_query = "SELECT banlist FROM user_banlist WHERE user_id = :user_id"
    extract_query_result = db_cursor.execute(extract_query, extract_query_params)
    rows = db_cursor.fetchall()
    
    if len(rows) == 0:
        return []
    
    banlist_list_form = convert_banlist_to_list_form(rows[0][0])
    

    return banlist_list_form

# Funtion to insert the banlist into the db
def insert_banlist_into_db(user_id, current_banlist, db_conn, db_cursor):
    """_summary_
    Inserts the provided banlist into the user_banlist table for the specified user_id
    Args:
        user_id (string): the user_id of the user whose banlist we want to update
        current_banlist (string): the banlist that is to be inserted into the table 
        db_conn (_type_): connection to the database
        db_cursor (_type_): cursor for the database
    """
    if current_banlist == None:
        raise error.InputError("Attempting to insert a non-existent banlist")
    # Check if the user_id has a corresponding banlist 
    check_query_params = {
        "user_id": user_id
    }
    
    check_query = "SELECT * FROM user_banlist WHERE user_id = :user_id"
    check_query_results = db_cursor.execute(check_query, check_query_params)
    rows = db_cursor.fetchall()
    
    # If no rows are returned i.e. a user_id does not yet exist for the user
    if len(rows) == 0:
        # Have to insert a row for the given user_id and their banlist
        insert_query_params = {
            "user_id": user_id,
            "banlist": current_banlist
        }

        insert_sql_query = "INSERT INTO user_banlist VALUES (:user_id, :banlist)"
        
        try:
            db_cursor.execute(insert_sql_query, insert_query_params)
            db_conn.commit()
        except sqlite3.IntegrityError as e:
            raise error.InputError(e)
    else:
        # Have to simply update the banlist column for the user_id
        update_query_params = {
            "user_id": user_id,
            "banlist": current_banlist
        }
        
        update_sql_query = "UPDATE user_banlist SET banlist = :banlist WHERE user_id = :user_id";
        
        try:
            db_cursor.execute(update_sql_query, update_query_params)
            db_conn.commit()
        except sqlite3.IntegrityError as e:
            raise error.InputError(e)
        
def get_banlist_user_details(current_banlist, db_conn, db_cursor):
    """_summary_
    Gets the user details such as first name, last name and email 
    about the users in the current banlist
    Args:
        current_banlist (list): the banlist that is to be inserted into the table 
        db_conn (_type_): connection to the database
        db_cursor (_type_): cursor for the database
    """
    list_of_user_details = []
    
    for user in current_banlist:
        sql_params = {
            "user_id": user
        }
        sql_query = """SELECT user_id, first_name, last_name, email
                       FROM users
                       WHERE user_id = :user_id"""
                       
        result = db_cursor.execute(sql_query, sql_params)
        rows = result.fetchone()
        print(rows)
        if rows == None:
             return {"banlist_user_details": []}
        details_dict = {
            "user_id": rows[0],
            "first_name": rows[1],
            "last_name": rows[2],
            "email": rows[3]
        }
        
        list_of_user_details.append(details_dict)
        
    return {"banlist_user_details": list_of_user_details}