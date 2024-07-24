import sys
import os
import sqlite3
import error
import poster_image

DB_PATH = "backend/db/mydb.db"

# list_format - [2,3,4,5]
# db_form - 2,3,4,5

# When adding and removing from the wishlist, we will deal with the wishlist in
# the python list format referred to as 'list_format'. 
# i.e. [2,3,4,5] where 2,3,4 and 5 are the tconst values on the wishlist.

# When storing the wishlist it will be stored in the user_wishlist as 
# comma separated values referred to as the 'db_form'
# i.e. [2,3,4,5] will be stored as 2,3,4,5 in the 'wishlist' column

    
def create_wish_list():
    """_summary_
    Creates an empty wishlist and returns it
    Returns:
        list: empty wishlist in the list format
    """
    return []

def add_to_wish_list(current_wish_list, tconst):
    """_summary_
    Adds a tconst value to the current wishlist.
    Args:
        current_wish_list (list): the wishlist that currently exists for the user 
        tconst (string): the tconst value that is to be added to the current wishlist

    Returns:
        current_wish_list (list): Returns an updated list 
                                containing the new tconst that was added. 
    """
    updated_wish_list = current_wish_list.append(tconst)
    return current_wish_list
    
def remove_from_wish_list(current_wish_list, tconst):
    """_summary_
    Removes a tconst value from the current wishlist.
    Args:
        current_wish_list (list): the wishlist that currently exists for the user 
        tconst (string): the tconst value that is to be removed from the current wishlist

    Returns:
        current_wish_list (list): Returns an updated list without the removed tconst. 
    """
    updated_wish_list = current_wish_list.remove(tconst)
    return current_wish_list
    
def convert_wish_list_to_db_form(current_wish_list):
    """_summary_
    Convert the wish list from a list in python to a CSV format.
    ['13', '25', '37', '44'] -> '13,25,37,44'
    Args:
        current_wish_list (list): the wishlist that currently exists for the user in the python list format

    Returns:
        string: a string/db_form of the wishlist is returned
    """
    return ','.join(current_wish_list)
    
def convert_wish_list_to_list_form(current_wish_list):
    """_summary_
    Convert the wish list from a CSV format to a list in python.
    '13,25,37,44' -> ['13', '25', '37', '44']
    Args:
        current_wish_list (string): the wishlist that currently exists for the user in the csv string/db_form

    Returns:
        list: a python list format of the wishlist is returned.
    """
    list_form = current_wish_list.rsplit(',')
    return list_form

def insert_wish_list_into_db(user_id, current_wish_list, db_conn, db_cursor):
    """_summary_
    Inserts the provided wishlist into the user_banlist table for the specified user_id
    Args:
        user_id (string): the user_id of the user whose wishlist we want to update
        current_wish_list (string): the wishlist that is to be inserted into the table 
        db_conn (_type_): connection to the database
        db_cursor (_type_): cursor for the database
    """
    # If a row does not exist for the user_id --> INSERT
    check_query_params = {
        "user_id": user_id
    }
    check_query = "SELECT * FROM user_wishlist WHERE user_id = :user_id"
    check_query_result = db_cursor.execute(check_query, check_query_params)
    rows = db_cursor.fetchall()
    
    if len(rows) == 0:
        # If a row does not exist for the user_id --> INSERT
        sql_params = {
        "wish_list_string": current_wish_list,
        "user_id": user_id
        }
        
        sql_query = "INSERT INTO user_wishlist VALUES (:user_id, :wish_list_string)"
    else:
        # If a row exists for the user_id --> UPDATE
        sql_params = {
        "wish_list_string": current_wish_list,
        "user_id": user_id
        }
        
        sql_query = "UPDATE user_wishlist SET wishlist = :wish_list_string where user_id = :user_id"
    
    try:
        db_cursor.execute(sql_query, sql_params)
        db_conn.commit()
    except sqlite3.IntegrityError as e:
        raise error.InputError(e)

def extract_wish_list_from_db(user_id, db_conn, db_cursor):
    """_summary_
    Extracts the user's wish list from the database based on user_id 
    and converts it to a python list and returns the list.
    Args:
        user_id (string): the user_id of the user whose wishlist we want to extract
        db_conn (_type_): connection to the database
        db_cursor (_type_): cursor for the database

    Returns:
        list: the wishlist for the user in the python list format.
    """
    sql_query = "SELECT wishlist FROM user_wishlist WHERE user_id = {}".format(user_id)
    result_wish_list = db_cursor.execute(sql_query)
    # returns a csv string of the wishlist.
    rows = db_cursor.fetchall()

    if len(rows) == 0:
        return []
    wish_list_list_form = convert_wish_list_to_list_form(rows[0][0])
    return wish_list_list_form

def remove_from_wish_list(current_wish_list, tconst):
    """_summary_
    Removes a tconst value from the current wishlist.
    Args:
        current_wish_list (list): the wishlist that currently exists for the user 
        tconst (string): the tconst value that is to be removed from the current wishlist

    Returns:
        current_wish_list (list): Returns an updated list without the removed tconst. 
    """
    tconst = str(tconst)

    if current_wish_list == []:
        raise error.InputError("Wishlist does not exist for user")

    if tconst in current_wish_list:
        current_wish_list.remove(tconst)
    elif tconst not in current_wish_list:
        raise error.InputError("Attempting to remove a movie that is not in the wishlist")

    return current_wish_list

def show_wish_list_movie_data(rows, db_conn, db_cursor):
    """_summary_
    Returns a list of the movie details such as title, year,
    genre, average rating given the user's wishlist.
    Args:
        rows (list): list of the tconst of the movies from the user's wishlist
        db_conn (_type_): connection to the database
        db_cursor (_type_): cursor for the database

    Returns:
        dictionary: a dictionary containing a list of the movie details for movies in the user's wishlist
    """
    '''
    Returns a list of the movie details such as title, year,
    genre, average rating given the user's wishlist.
    '''
    
    movie_data_list = []
    
    for tconst in rows:
        sql_param = {
            "tconst": tconst
        }
        sql_query = """SELECT a.tconst, a.primaryTitle, a.startYear, a.genres, b.averageRating 
                    FROM title_basics a INNER JOIN title_ratings b ON a.tconst = b.tconst WHERE a.tconst = :tconst""" 
        # shouldnt use format() for sql queries. Look at examples from auth on how I structure the query with parameters.
        db_cursor.execute(sql_query, sql_param)
        movie_data = db_cursor.fetchall() 
        # example of movie_data: movie_data = [(tt123, 'The Godfather', 2000, 'Drama', 8), (tt456, 'The Godfather: Part II', 2002, 'Drama', 8), ...]

        # Unbind the tuples from the result and put it into a dictionary.
        if movie_data is None:
            return []

        movie_data_dict = {}
        for row in movie_data:
            tconst = row[0]
            movie_data_dict["tconst"] = tconst
            movie_data_dict["primaryTitle"] = row[1]
            movie_data_dict["startYear"] = row[2]
            movie_data_dict["genres"] = row[3]
            movie_data_dict["averageRating"] = row[4]

            image = poster_image.get_movie_poster(tconst)
            movie_data_dict["poster_image"] = image
        
        movie_data_list.append(movie_data_dict)

        # movie_data_list will look like this:
        # [{'tconst': 'tt123', 'primaryTitle': 'The Godfather','startYear': 2000, 'genres': 'Drama', 'averageRating': 8},
        #  {'tconst': 'tt456', 'primaryTitle': 'The Godfather: Part II','startYear': 2002, 'genres': 'Drama', 'averageRating': 8}]
        
    if movie_data_list == None:
        return {"wishlist": []}

    return {"wishlist": movie_data_list}