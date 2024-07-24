
import poster_image
import concurrent.futures
import tmdb_api
import kids_friendly_mode

DB_PATH = "backend/db/imdb.db"

def movie_details(row):
    tconst = row[0]
    image = poster_image.get_movie_poster(str(tconst))
    is_age_safe = False
    return {
        "tconst": row[0],
        "primaryTitle": row[1], 
        "year": row[2],
        "genres": row[3],
        "rating": row[4],
        "poster_image": image,
        "is_age_safe": is_age_safe
    }

def movie_details_kids(row):
    tconst = row[0]
    image = poster_image.get_movie_poster(str(tconst))
    is_age_safe = False
    try:
        is_age_safe = tmdb_api.check_movie_is_age_safe(tconst)
    except Exception as e:
        pass
    return {
        "tconst": row[0],
        "primaryTitle": row[1], 
        "year": row[2],
        "genres": row[3],
        "rating": row[4],
        "poster_image": image,
        "is_age_safe": is_age_safe
    }

def search_movie (user_id, user_search, db_conn, db_cursor):
    """
    Searches for movies which contain the user_search string

    Parameters:
        user_search: string to search for
        user_id: the users id
        db_conn: database connection
        db_cursor: database cursor

    Returns:
        list of tuples containing the tconst, primaryTitle, genres, year, averageRating and posterImage
    """

    # construct SQL query
    sql_query = """select a.tconst, a.primaryTitle, a.startYear, a.genres, b.averageRating 
        FROM title_basics a INNER JOIN title_ratings b 
        ON a.tconst = b.tconst
        WHERE primaryTitle LIKE '%{}%' AND titleType = "movie" limit 100 collate nocase""".format(user_search)
    
    # connect to database and collect all tconst for movies which match 
    result = db_cursor.execute(sql_query)
    rows = result.fetchall()

    if rows == None:
        return {"movies": []}
    
    # Unpack rows into dictionary values
    list_of_movies = []

    is_child_user = kids_friendly_mode.is_user_child(user_id, db_conn, db_cursor)
    if is_child_user:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            movie_details_obj = executor.map(movie_details_kids, rows)
            for movie in movie_details_obj:
                if movie['is_age_safe']:
                    list_of_movies.append({
                        "tconst": movie["tconst"],
                        "primaryTitle": movie["primaryTitle"],
                        "year": movie['year'],
                        "genres": movie['genres'],
                        "rating": movie['rating'],
                        "poster_image": movie['poster_image'],
                    })
                    # list_of_movies.append(movie)


        result_dict = {
            "movies": list_of_movies
        }
        return result_dict


    with concurrent.futures.ThreadPoolExecutor() as executor:
        movie_details_obj = executor.map(movie_details, rows)
        for movie in movie_details_obj:
            list_of_movies.append(movie)

    return {"movies": list_of_movies}


def search_genre (user_id, user_search, db_conn, db_cursor):
    """
    Searches for movies associated with a genre

    Parameters:
        user_search: genre to search for
        user_id: the users id
        db_conn: database connection
        db_cursor: database cursor
    
    Returns:
        A list of tuples containing tconst, primaryTitle, year, genres, rating and posterImage
        for movies for the associated genre
    """

    # ~ Andre's Version
    sql_query = """select a.tconst, a.primaryTitle, a.startYear, a.genres, b.averageRating
    FROM title_basics a INNER JOIN title_ratings b
    ON a.tconst = b.tconst
    WHERE a.genres LIKE '%{}%' limit 50 collate nocase""".format(user_search)

    # connect to database and collect all tconst for movies which match 
    result = db_cursor.execute(sql_query)
    rows = result.fetchall()

    if rows == None:
        return {"movies": []}
    
    # Unpack rows into dictionary values
    list_of_movies_for_genre = []
    is_child_user = kids_friendly_mode.is_user_child(user_id, db_conn, db_cursor)
    if is_child_user:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            movie_details_obj = executor.map(movie_details_kids, rows)
            for movie in movie_details_obj:
                if movie['is_age_safe']:
                    list_of_movies_for_genre.append({
                        "tconst": movie["tconst"],
                        "primaryTitle": movie["primaryTitle"],
                        "year": movie['year'],
                        "genres": movie['genres'],
                        "rating": movie['rating'],
                        "poster_image": movie['poster_image'],
                    })

        result_dict = {
            "movies": list_of_movies_for_genre
        }
        return result_dict
    

    with concurrent.futures.ThreadPoolExecutor() as executor:
        movie_details_obj = executor.map(movie_details, rows)
        for movie in movie_details_obj:
            list_of_movies_for_genre.append(movie)


    return {"movies": list_of_movies_for_genre}


def search_year (user_id, user_search, db_conn, db_cursor):
    """
    Searches for movies released in the year inputted by the user

    Parameters:
        user_id: a users id
        user_search: year to search for
        db_conn: database connection
        db_cursor: database cursor
    
    Returns:
        A list of tuples containing tconst, primaryTitle, year, genres, rating and posterImage
        for movies released in the associated year
    """

    sql_query = """select a.tconst, a.primaryTitle, a.startYear, a.genres, b.averageRating
    FROM title_basics a INNER JOIN title_ratings b
    ON a.tconst = b.tconst
    WHERE a.startYear = {} limit 50 collate nocase""".format(user_search)

       # connect to database and collect all tconst for movies which match 
    result = db_cursor.execute(sql_query)
    rows = result.fetchall()

    if rows == None:
        return {"movies": []}
    
    # Unpack rows into dictionary values
    list_of_movies_for_year = []
    is_child_user = kids_friendly_mode.is_user_child(user_id, db_conn, db_cursor)
    if is_child_user:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            movie_details_obj = executor.map(movie_details_kids, rows)
            for movie in movie_details_obj:
                if movie['is_age_safe']:
                    list_of_movies_for_year.append({
                        "tconst": movie["tconst"],
                        "primaryTitle": movie["primaryTitle"],
                        "year": movie['year'],
                        "genres": movie['genres'],
                        "rating": movie['rating'],
                        "poster_image": movie['poster_image'],
                    })

        result_dict = {
            "movies": list_of_movies_for_year
        }
        return result_dict
    
    

    with concurrent.futures.ThreadPoolExecutor() as executor:
        movie_details_obj = executor.map(movie_details, rows)
        for movie in movie_details_obj:
            list_of_movies_for_year.append(movie)


    return {"movies": list_of_movies_for_year}


def search_by_actor (user_id, user_search, db_conn, db_cursor):
    """
    Searches for movies which contain the particular actor/actressed searched by the user

    Parameters:
        user_id: the users id
        user_search: actor name string to search for
        db_conn: database connection
        db_cursor: database cursor
    
    Returns:
        A list of tuples containing tconst, primaryTitle, year, genres, rating, posterImage and isAgeSafe boolean
        for movies associated with the appropriate actor/actress given by the user
    """
    sql_params = {
        "user_search": user_search
    }
    
    sql_query = """SELECT knownForTitles 
                FROM name_basics_fts 
                WHERE primaryName 
                MATCH :user_search"""
    
    result = db_cursor.execute(sql_query,sql_params)
    rows = result.fetchall()

    # Check if the rows are empty
    if rows == []:
        return {"movies": []}
    
    # Extract the csv format to a list 
    csv_movies = rows[0][0]
    list_of_tconst = csv_movies.rsplit(',')
    
    list_of_movies = []

    is_child_user = kids_friendly_mode.is_user_child(user_id, db_conn, db_cursor)
    if is_child_user:
        for tconst in list_of_tconst:
            sql_movie_params = {
            "tconst": tconst
            }
            sql_query_movie = """SELECT a.tconst, a.primaryTitle, a.startYear, a.genres, b.averageRating 
                                FROM title_basics a INNER JOIN title_ratings b 
                                ON a.tconst = b.tconst
                                WHERE a.tconst = :tconst"""
                                
            result = db_cursor.execute(sql_query_movie, sql_movie_params)
            rows = result.fetchone()
            
            tconst = rows[0]
            is_age_safe = tmdb_api.check_movie_is_age_safe(tconst)
            if (is_age_safe):

                image = poster_image.get_movie_poster(str(tconst))
                details_dict = {
                    "tconst": rows[0],
                    "primaryTitle": rows[1], 
                    "year": rows[2],
                    "genres": rows[3],
                    "rating": rows[4],
                    "poster_image": image,
                    "is_age_safe": is_age_safe
                }
                
                list_of_movies.append(details_dict)

        return {"movies": list_of_movies}


    
    for tconst in list_of_tconst:
        sql_movie_params = {
        "tconst": tconst
        }
        sql_query_movie = """SELECT a.tconst, a.primaryTitle, a.startYear, a.genres, b.averageRating 
                             FROM title_basics a INNER JOIN title_ratings b 
                             ON a.tconst = b.tconst
                             WHERE a.tconst = :tconst"""
                             
        result = db_cursor.execute(sql_query_movie, sql_movie_params)
        rows = result.fetchone()
        
        tconst = rows[0]
        image = poster_image.get_movie_poster(str(tconst))
        details_dict = {
            "tconst": rows[0],
            "primaryTitle": rows[1], 
            "year": rows[2],
            "genres": rows[3],
            "rating": rows[4],
            "poster_image": image,
            "is_age_safe": False
        }
        
        list_of_movies.append(details_dict)



           
    return {"movies": list_of_movies}
