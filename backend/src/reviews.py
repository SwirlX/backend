import sys
import os
import sqlite3
import error
import utils
import admins
import banlist


def review_exists(review_id, db_cursor):
    """
    Check if the review_id exists in the database

    Parameters:
        review_id: The review id
        db_cursor: db cursor

    Returns:
        bool
    """
    db_cursor.execute('SELECT review_id FROM reviews WHERE review_id =?', (review_id,))
    movie_review_id = db_cursor.fetchone()

    return movie_review_id is not None


def create_review(user_id, tconst, rating, review_text, db_conn, db_cursor):
    """
    Create a review

    Parameters:
        user_id: The id of the user creating the review
        tconst: The tconst movie id of the movie the review is being made on
        rating: The rating made with the review
        review_text: The content of the review text
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        None
    """
    
    if not utils.user_exists(user_id, db_conn, db_cursor):
        raise error.InputError("User not found")
    
    if not utils.movie_exists(tconst, db_conn, db_cursor):
        raise error.DatabaseError("Movie does not exist in database")

    try:
        db_cursor.execute('INSERT INTO reviews (user_id, tconst, rating, review_text) VALUES (?,?,?,?)', (user_id, tconst, rating, review_text))
        db_conn.commit()
    except Exception as e:
        raise error.DatabaseError("Error creating review: " + str(e))


def get_review_id(user_id, tconst, rating, review_text, db_conn, db_cursor):
    """
    Get the review id of a review

    Parameters:
        user_id: The id of the user that created the review
        tconst: The tconst movie id of the movie the review was made on
        rating: The rating made with the review
        review_text: The content of the review text
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        string: review_id
    """

    if not utils.user_exists(user_id, db_conn, db_cursor):
        raise error.InputError("User not found")
    
    if not utils.movie_exists(tconst, db_conn, db_cursor):
        raise error.DatabaseError("Movie does not exist in database")
    

    db_cursor.execute('SELECT review_id FROM reviews WHERE user_id =? AND tconst =? AND rating =? AND review_text =?', (user_id, tconst, rating, review_text))
    review_id = db_cursor.fetchone()
    if review_id is None:
        raise error.InputError("Review not found in database")
    
    return review_id[0]

def get_review(review_id, db_conn, db_cursor):
    """
    Return all details of a review given the review id

    Parameters:
        review_id: The review id of the review to retrieve

    Returns:
        Dict: {user_id, tconst, rating, review_text}
    """

    if not review_exists(review_id, db_cursor):
        raise error.DatabaseError("Review not found in database")

    db_cursor.execute('SELECT user_id, tconst, rating, review_text FROM reviews WHERE review_id =?', (review_id,))
    review = db_cursor.fetchone()
    
    return {
        "user_id": review[0],
        "tconst": review[1],
        "rating": review[2],
        "review_text": review[3]
    }

    
# get all reviews for a movie
def get_all_movie_reviews(tconst, user_id, db_conn, db_cursor):
    """
    Gets all movie reviews for a given movie

    Parameters:
        tconst: The tconst movie id of the movie
        user_id: The id of the user requesting the reviews
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        Dict: [reviews: {review_id, user_id, tconst, rating, review_text}]
    """


    user_is_admin = False 
    current_user_banlist = []
    if (user_id != ""): 
        user_is_admin = admins.user_is_admin(user_id, db_conn, db_cursor)
        current_user_banlist = banlist.extract_banlist_from_db(user_id, db_conn, db_cursor)
    
    
    if not utils.movie_exists(tconst, db_conn, db_cursor):
        raise error.DatabaseError("Movie does not exist in database")

    db_cursor.execute('SELECT * FROM reviews WHERE tconst =?', (tconst,))
    reviews = db_cursor.fetchall()
    reviews_dict_list = []

    # Unpack list of tuples in reviews variables into a list of dictionaries
    for review in reviews:
        if str(review[1]) not in current_user_banlist or user_is_admin:
            review_dict = {}
            review_dict["review_id"] = review[0]
            review_dict["user_id"] = review[1]
            review_dict["tconst"] = review[2]
            review_dict["rating"] = review[3]
            review_dict["review_text"] = review[4]

            reviews_dict_list.append(review_dict)

    return {"reviews": reviews_dict_list} 


# update/edit a review
def update_review_text(review_id, review_text, db_conn, db_cursor):

    # Check if the review_id exists in the database
    if not review_exists(review_id, db_cursor):
        raise error.DatabaseError("Review not found in database")

    try:
        db_cursor.execute('UPDATE reviews SET review_text =? WHERE review_id =?', (review_text, review_id))
        db_conn.commit()
    except Exception as e:
        raise error.DatabaseError("Error updating review: " + str(e))
    

def delete_review(current_user_id, review_id, db_conn, db_cursor):
    """
    Delete a review given the review id

    Parameters:
        current_user_id: User id of the current user trying to delete review
        review_id: The id of the review
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        None
    """
    if not review_exists(review_id, db_cursor):
        raise error.DatabaseError("Review not found in database")

    cur = db_cursor.execute('SELECT user_id FROM reviews WHERE review_id = ?', (review_id,))
    reviewers_user_id = cur.fetchone()[0]

    if current_user_id != reviewers_user_id:
        raise error.AccessError("User did not create the review")

    try:
        db_cursor.execute('DELETE FROM reviews WHERE review_id =?', (review_id,))
        db_conn.commit()
    except Exception as e:
        raise error.DatabaseError("Error deleting review: " + str(e))
    
def delete_review_as_admin(current_user_id, review_id, db_conn, db_cursor):
    """
    Delete a review as an admin given the review id. Admin can delete any review

    Parameters:
        current_user_id: User id of the current user trying to delete review
        review_id: The id of the review
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        None
    """

    if not admins.user_is_admin(current_user_id, db_conn, db_cursor):
        raise error.AdminError("User is not an admin")

    if not review_exists(review_id, db_cursor):
        raise error.DatabaseError("Review not found in database")

    try:
        db_cursor.execute('DELETE FROM reviews WHERE review_id =?', (review_id,))
        db_conn.commit()
    except Exception as e:
        raise error.DatabaseError("Error deleting review: " + str(e))
    
def get_user_reviews(user_id, db_conn, db_cursor):
    """
    Get all the reviews of a user

    Parameters:
        user_id: User id of the current user
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        Dict: [reviews: {review_id, user_id, tconst, rating, review_text}]
    """

    if not utils.user_exists(user_id, db_conn, db_cursor):
        raise error.InputError("User not found")

    db_cursor.execute('SELECT * FROM reviews WHERE user_id =?', (user_id,))
    reviews = db_cursor.fetchall()
    reviews_dict_list = []

    # Unpack list of tuples in reviews variables into a list of dictionaries
    for review in reviews:
        review_dict = {}
        review_dict["review_id"] = review[0]
        review_dict["user_id"] = review[1]
        review_dict["tconst"] = review[2]
        review_dict["rating"] = review[3]
        review_dict["review_text"] = review[4]

        reviews_dict_list.append(review_dict)

    return {"reviews": reviews_dict_list}

def get_average_movie_ratings_user(tconst, user_id, db_conn, db_cursor):
    """
    Get the average rating of a movie. 
    Will ignore ratings of uses in the banlist

    Parameters:
        tconst: The tconst movie id of the movie
        user_id: User id of the current user
        db_conn: db connection
        db_cursor: db cursor

    Returns:
        Dict: [reviews: {review_id, user_id, tconst, rating, review_text}]
    """

    user_is_admin = False 
    current_user_banlist = []
    if (user_id != ""): 
        user_is_admin = admins.user_is_admin(user_id, db_conn, db_cursor)
        # NEW - Get the current users_id's banlist
        current_user_banlist = banlist.extract_banlist_from_db(user_id, db_conn, db_cursor)

    if not utils.movie_exists(tconst, db_conn, db_cursor):
        raise error.DatabaseError("Movie does not exist in database")

    db_cursor.execute('SELECT * from reviews WHERE tconst = ?', (tconst,))
    reviews = db_cursor.fetchall()
    reviews_dict_list = []

    for review in reviews:
        if str(review[1]) not in current_user_banlist or user_is_admin:
            review_dict = {}
            review_dict["review_id"] = review[0]
            review_dict["user_id"] = review[1]
            review_dict["tconst"] = review[2]
            review_dict["rating"] = review[3]
            review_dict["review_text"] = review[4]

            reviews_dict_list.append(review_dict)

    sum_of_ratings = 0
    print(reviews_dict_list)
    for r in reviews_dict_list:
        if (r["rating"] == ""):
            continue
        sum_of_ratings += float(r["rating"])
        print(sum_of_ratings)
    if (len(reviews_dict_list) == 0):
        average_rating = float(sum_of_ratings)
    else:
        average_rating = float(sum_of_ratings/len(reviews_dict_list))

    average_rating = round(average_rating, 1)

    return {"average_rating" : average_rating}