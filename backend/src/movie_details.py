import sys
import os
from json import loads
import hashlib
import sqlite3
import error
import poster_image
import concurrent.futures
import tmdb_api
import kids_friendly_mode


def get_landing_page_random_movie_details(user_id, db_conn, db_cursor):
    """
    Get a random movie from the landing page
    :param db_conn: database connection
    :param db_cursor: database cursor
    :return: a dictionary containing the movie details
    :raises DatabaseError: if no movies are found
    """
    is_child_user = kids_friendly_mode.is_user_child(user_id, db_conn, db_cursor)

    if is_child_user:
        query = "SELECT tb.tconst, tb.primaryTitle, tb.startYear FROM title_basics tb JOIN title_ratings tr ON tb.tconst = tr.tconst WHERE random() % 100 = 0 AND titleType ='movie' AND isAdult = 0 AND tr.numVotes > 10000 LIMIT 500;"
        db_cursor.execute(query)
        rows = db_cursor.fetchall()
        
        if len(rows) == 0:
            raise error.DatabaseError("No movies found, try again")
    
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            movie_details_obj = executor.map(create_movie_dict_kids, rows)
            for movie in movie_details_obj:
                if movie['is_age_safe']:
                    results.append({
                        "tconst": movie['tconst'],
                        "primaryTitle": movie['primaryTitle'],
                        "startYear": movie['startYear'],
                        "poster_image": movie['poster_image'] 
                    })
    
        result_dict = {
            "results": results
        }
        return result_dict

    query = "SELECT tb.tconst, tb.primaryTitle, tb.startYear FROM title_basics tb JOIN title_ratings tr ON tb.tconst = tr.tconst WHERE random() % 500 = 0 AND tb.titleType ='movie' AND tb.isAdult = 0 AND tr.numVotes > 5000  LIMIT 400;"
    db_cursor.execute(query)
    rows = db_cursor.fetchall()
    
    if len(rows) == 0:
        raise error.DatabaseError("No movies found, try again")

    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        movie_details_obj = executor.map(create_movie_dict, rows)
        for movie in movie_details_obj:
            results.append(movie)

    result_dict = {
        "results": results
    }
    return result_dict

def create_movie_dict(row):
    """
    Creates a response dictionary for movie details

    Parameters:
        row: The tuple containing the details

    Returns:
        Dict
    """
    tconst = row[0]
    movie_poster_img = poster_image.get_movie_poster(tconst)
    is_age_safe = False

    return {
        "tconst": tconst,
        "primaryTitle": row[1],
        "startYear": row[2],
        "poster_image": movie_poster_img,
        "is_age_safe": is_age_safe
    }


def create_movie_dict_kids(row):
    """
    Creates a response dictionary for movie details that are kid friendly

    Parameters:
        row: The tuple containing the details

    Returns:
        Dict
    """
    tconst = row[0]
    movie_poster_img = poster_image.get_movie_poster(tconst)
    is_age_safe = False
    try:
        is_age_safe = tmdb_api.check_movie_is_age_safe(tconst)
    except Exception as e:
        pass
        # print(f'Movie {row[1]}: Error: {e} ')

    return {
        "tconst": tconst,
        "primaryTitle": row[1],
        "startYear": row[2],
        "poster_image": movie_poster_img,
        "is_age_safe": is_age_safe
    }


def get_movie_details(tconst, db_conn, db_cursor):
    """
    Get basic movie details

    Parameters:
        tconst: The tconst movie id

    Returns:
        Dict: {title, year, genres}
    """
    res = db_cursor.execute("SELECT primaryTitle, startYear, genres FROM title_basics WHERE tconst =?", (tconst,))
    rows = res.fetchone()

    if rows is None:
        raise error.DatabaseError("Movie doesn't exist in the database")
    
    return {
                "title": rows[0],
                "year": rows[1], 
                "genres": rows[2]
            }

def get_further_movie_details(tconst):
    """
    Get further movie details such as cast, directors, publications

    Parameters:
        tconst: The tconst movie id

    Returns:
        Dict
    """
    return tmdb_api.get_all_movie_details(tconst)

    
def get_movie_crew(tconst, db_conn, db_cursor):
    """
    Get crew members of a movie

    Parameters:
        tconst: The tconst movie id

    Returns:
        Dict: [{nconst, role, character, name, birthYear}]
    """
    res = db_cursor.execute("SELECT  tp.nconst , tp.category, tp.characters, names.primaryName, names.birthYear \
                                FROM title_principals tp JOIN name_basics names \
                                    ON tp.nconst = names.nconst \
                                WHERE tp.tconst = ?", 
                            (tconst,))
    rows = res.fetchall()

    # Unpack the rows
    crew_list = []
    for row in rows:
        crew_member = {
            "nconst": row[0],
            "role": row[1],
            "character": row[2],
            "name": row[3],
            "birthYear": row[4]
        }
        crew_list.append(crew_member)

    return {"crew": crew_list}
