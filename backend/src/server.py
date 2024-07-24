"""
Flask Web Server

This file defines a Flask web server that handles HTTP requests and responses.
It provides endpoints for various operations such as handling user authentication,
retrieving and manipulating data from a database, and performing other core application logic
for the movie finder system

Author: Name-this-group

Requirements:
- Python 3.7 or higher. Ideally Python 3.9
- Other dependencies outlined in requirements.txt

Usage:
- Run this script to start the server
- Access the endpoints using a web browser or an HTTP client (e.g., Postman)
- Run by running the command `python3 server.py`
"""

import sys
import os
import data
from json import dumps
from flask import Flask, request, g, jsonify
from flask_cors import CORS
from flask import send_file
import urllib.request
import urllib.error
import auth
import utils
import sqlite3
import search
import forum
import movie_details
import wishlist
import banlist
import reviews
import users
import chatbot
from werkzeug.exceptions import HTTPException
import tmdb_api
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import admins
import kids_friendly_mode

CLIENT = MongoClient(data.MONGODB_KEY, server_api=ServerApi('1'))
APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

@APP.before_request
def db_setup():
    """
    This is the setup function that will set up the
    """
    g.db = sqlite3.connect(utils.DB_PATH)
    g.cursor = g.db.cursor()
@APP.before_first_request
def setup():

    """
    Creates a default admin account before the first request
    """
    utils.create_default_admin()

@APP.teardown_request
def db_teardown(exception):
    """
    Teardown function to close the connection to the db
    """
    if hasattr(g, 'db'):
        g.cursor.close()
        g.db.close()

@APP.errorhandler(HTTPException)
def handle_error(e):
    """
    Error handler to return an error as a response
    if there is an exception raised or error on the server
    """
    APP.logger.error(str(e))
    response = jsonify({'error': str(e)})
    response.status_code = e.code
    return response

@APP.route("/auth/register", methods=['POST'])
def auth_register():
    """
    Register a new user given an email and password, first and last name and D.O.B

    Parameters:
        email
        password
        first_name
        last_name
        dob
        age

    Response:
       {token}
    """
    
    data = request.get_json()
    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    age = data['age']
    user = auth.register_user(email, password, first_name, last_name, dob, age, g.db, g.cursor)
    print(user)
    return dumps(user)


@APP.route("/auth/register-child", methods=['POST'])
def auth_register_child():
    """
    Register a new child account given an email and password, first and last name and D.O.B

    Parameters:
        email
        password
        first_name
        last_name
        dob
        age

    Response:
        {is_success}
    """
    data = request.get_json()
    email = data['email']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    age = data['age']
    user = auth.register_user_child(email, password, first_name, last_name, dob, age, g.db, g.cursor)
    print(user)
    return dumps(user)

@APP.route("/auth/login", methods=['POST'])
def auth_login():
    """
    Log the user into the application given an email and password.

    Parameters:
        email
        password

    Response:
        {token}
    """
    data = request.get_json()
    print(data)
    email = data['email']
    password = data['password']
    user = auth.login_user(email, password, g.db, g.cursor)
    print(user['user_id'])
    admin = admins.user_is_admin(str(user['user_id']), g.db, g.cursor)
    user["admin"] = admin
    return dumps(user)

@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    """
    Log the user into the application given an email and password.

    Parameters:
        token: User's session token

    Response:
        {is_success}
    """
    data = request.get_json()
    token = data['token']
    success_response = auth.logout_user(token, g.db, g.cursor)
    return dumps(success_response)

@APP.route("/user/get-user-details/<user_id>", methods=['GET'])
def get_user_details(user_id): 
    """
    Get the details of a user given their user_id

    Parameters:
        user_id (path param)

    Response:
        {first_name, last_name, email, dob, token, is_admin, is_child}
    """
    user_details = users.get_user_details(user_id, g.db, g.cursor)
    return dumps(user_details)

@APP.route("/user/get-all-users", methods=['GET'])
def get_all_users():
    """
    Get all users in the database

    Parameters:
        None

    Response:
        [{user_id, first_name, last_name, email, dob, token, is_admin, is_child}]
    """
    all_users = users.get_all_users(g.db, g.cursor)
    return dumps(all_users)


@APP.route("/search/<keyword>", methods=['GET'])
def searchMovie(keyword):
    """
    Given a keyword, returns movies which relate to keyword.

    Parameters:
        keyword (path param): Keyword to search by

    Response:
        [{tconst, primaryTitle, year, genres, rating, poster_image}]
    """
    user_id = request.args.get('user_id')
    search_results = search.search_movie(user_id, keyword, g.db, g.cursor)
    return dumps(search_results)

@APP.route("/search/genre/<genre_name>", methods=['GET'])
def searchGenre(genre_name):
    """
    Given a genre name, returns movies which is of that genre.

    Parameters:
        genre_name (path param): genre name to search by

    Response:
        [{tconst, primaryTitle, year, genres, rating, poster_image}]
    """
    user_id = request.args.get('user_id')
    search_results = search.search_genre(user_id, genre_name, g.db, g.cursor)
    return dumps(search_results)

@APP.route("/search/year/<year>", methods=['GET'])
def searchYear(year):
    """
    Given a year, returns movies which are released that year.

    Parameters:
        year (path param): year to search by

    Response:
        [{tconst, primaryTitle, year, genres, rating, poster_image}]
    """
    user_id = request.args.get('user_id')
    search_results = search.search_year(user_id, year, g.db, g.cursor)
    return dumps(search_results)
    
@APP.route("/search/by-actor/<actor>", methods=['GET'])
def search_movies_by_actor(actor):
    """
    Given an actors name, returns movies which that actor is known for.

    Parameters:
        actor (path param): actor to search by

    Response:
        [{tconst, primaryTitle, year, genres, rating, poster_image}]
    """
    user_id = request.args.get('user_id')
    search_results = search.search_by_actor(user_id, actor, g.db, g.cursor)
    return dumps(search_results)


@APP.route("/movie/get-movie-details/<tconst>", methods=['GET'])
def get_movie_details(tconst):
    """
    Given a tconst, returns basic details about the movie like name year and genre

    Parameters:
        tconst (path param): tconst movie id to get movie details for

    Response:
        {title, year, genres}
    """
    movie_details_dict = movie_details.get_movie_details(tconst, g.db, g.cursor)
    return dumps(movie_details_dict)

@APP.route("/movie/page-details/<tconst>", methods=["GET"])
def get_movie_page_details(tconst):
    """
    Given a tconst, returns further details about the movie that can be displayed
    on the movie details page, such as cast, directors, publications 

    Parameters:
        tconst (path param): tconst movie id to get movie details for

    Response:
        {get_further_movie_details, nconst, role, character, name, birthYear}
    """
    movie_page_details = movie_details.get_further_movie_details(tconst)
    return dumps(movie_page_details)
   
@APP.route("/auth/password_reset/request", methods=['POST'])
def auth_password_reset_request():
    """
    Send the authentication code to user's email for when the user attempts
    to change their password.

    Parameters:
        email

    Response:
        reset_code
    """
    data = request.get_json()
    email = data['email']
    user_reset_code = auth.password_reset_request(email, g.db, g.cursor)
    return dumps(user_reset_code)
    
    
@APP.route("/auth/password_reset/reset", methods=['POST'])
def auth_password_reset_reset():
    """
    To change the password over to the new password.

    Send the authentication code to user's email for when the user attempts
    to change their password.

    Parameters:
        email
        new_password

    Response:
        {is_success}
    """
    data = request.get_json()
    email = data['email']
    new_password = data['new_password']
    reseted = auth.password_reset_reset(email, new_password, g.db, g.cursor)
    # TO DO: No return required, double check
    return dumps(reseted)


@APP.route("/movies/get-random-movies", methods=['GET'])
def get_random_movies():
    """
    Get random list of movie titles and years

    Parameters:
        None

    Response:
        {tconst, primaryTitle, startYear, poster_image}
    """
    current_user_id = request.args.get('current_user_id')

    result = movie_details.get_landing_page_random_movie_details(current_user_id ,g.db, g.cursor)
    return dumps(result)


@APP.route("/wishlist/view", methods=['GET'])
def get_user_wishlist():
    """
    View the users wishlist

    Parameters:
        user_id

    Response:
        [{tconst, primaryTitle, startYear, genres, averageRating, poster_image}]
    """
    user_id = request.args.get('user_id')
    print(request.args)

    rows = wishlist.extract_wish_list_from_db(user_id, g.db, g.cursor)
    wishlist_movies = wishlist.show_wish_list_movie_data(rows, g.db, g.cursor)

    return dumps(wishlist_movies)


@APP.route("/wishlist/add", methods=['PUT'])
def add_to_user_wishlist():
    """
    Add to wishlist

    Parameters:
        user_id
        tconst

    Response:
        {is_success}
    """
    data = request.get_json()
    user_id = data['user_id']
    movie_tconst = data['tconst']

    curr_wishlist = wishlist.extract_wish_list_from_db(user_id, g.db, g.cursor)
    curr_wishlist = wishlist.add_to_wish_list(curr_wishlist, movie_tconst)
    curr_wishlist = wishlist.convert_wish_list_to_db_form(curr_wishlist)
    wishlist.insert_wish_list_into_db(user_id, curr_wishlist, g.db, g.cursor)

    return dumps({"is_success": True})


@APP.route("/wishlist/remove", methods=['PUT'])
def remove_user_wishlist():
    """
    Remove from wishlist

    Parameters:
        user_id
        tconst

    Response:
        {is_success}
    """
    data = request.get_json()
    user_id = data['user_id']
    movie_tconst = data['tconst']

    curr_wishlist = wishlist.extract_wish_list_from_db(user_id, g.db, g.cursor)
    curr_wishlist = wishlist.remove_from_wish_list(curr_wishlist, movie_tconst)
    curr_wishlist = wishlist.convert_wish_list_to_db_form(curr_wishlist)
    wishlist.insert_wish_list_into_db(user_id, curr_wishlist, g.db, g.cursor)

    return dumps({"is_success": True})


@APP.route("/banlist/add", methods=["PUT"])
def add_user_to_banlist():
    """
    Add a user to the banlist

    Parameters:
        user_id: The user id of the user trying to ban another user
        uder_id_to_ban: The id of the user to ban

    Response:
        {is_success}
    """
    data = request.get_json()
    user_id = data['user_id']
    user_id_to_ban = data['user_id_to_ban']
    
    curr_banlist = banlist.extract_banlist_from_db(user_id, g.db, g.cursor)
    curr_banlist = banlist.add_user_to_banlist(curr_banlist, user_id_to_ban)
    curr_banlist = banlist.convert_banlist_to_db_form(curr_banlist)
    banlist.insert_banlist_into_db(user_id, curr_banlist, g.db, g.cursor)
    
    return dumps({"is_success": True})

@APP.route("/banlist/remove", methods=["PUT"])
def remove_user_from_banlist():
    """
    Remove a user from the banlist

    Parameters:
        user_id: The user id of the current user
        user_id_to_remove: The id of the user to remove from ban list

    Response:
        {is_success}
    """
    data = request.get_json()
    user_id = data['user_id']
    user_id_to_remove = data['user_id_to_remove']
    
    curr_banlist = banlist.extract_banlist_from_db(user_id, g.db, g.cursor)
    curr_banlist = banlist.remove_user_from_banlist(curr_banlist, user_id_to_remove)
    curr_banlist = banlist.convert_banlist_to_db_form(curr_banlist)
    banlist.insert_banlist_into_db(user_id, curr_banlist, g.db, g.cursor)
    
    return dumps({"is_success": True})

@APP.route("/banlist/show", methods=['GET'])
def show_user_banlist():
    """
    Show a user banlist

    Parameters:
        user_id: The user id of the current user

    Response:
        [{user_id, first_name, last_name, email]}
    """
    user_id = request.args.get('user_id')
    curr_banlist = banlist.extract_banlist_from_db(user_id, g.db, g.cursor)
    curr_banlist = filter(None, curr_banlist)
    list_of_banlist_user_details = banlist.get_banlist_user_details(curr_banlist, g.db, g.cursor)
    
    return dumps(list_of_banlist_user_details)
    
@APP.route("/reviews/create", methods=['POST'])
def create_review():
    """
    Create a review

    Parameters:
        tconst: The tconst movie id of the movie to leave a review on
        user_id: The current user id
        review_text: The review text of the review
        rating: The rating left by the review

    Response:
        None
    """
    data = request.get_json()
    tconst = data['tconst']
    review_text = data['review_text']
    rating = data['rating']
    user_id = data['user_id']
    print(data)
    reviews.create_review(user_id, tconst, rating, review_text, g.db, g.cursor)
    return dumps({})

@APP.route("/reviews/get-review-id", methods=['GET'])
def get_review_id():
    """
    Get the review id of a review

    Parameters:
        tconst: The tconst movie id of the movie 
        user_id: The current user id
        review_text: The review text of the review
        rating: The rating left by the review

    Response:
        review_id: int
    """
    data = request.get_json()
    user_id = data['user_id']
    tconst = data['tconst']
    rating = data['rating']
    review_text = data['review_text']

    result = reviews.get_review_id(user_id, tconst, rating, review_text, g.db, g.cursor)
    return dumps(result)

@APP.route("/reviews/get-review", methods=['GET'])
def get_review():
    """
    Given a review id, get the review content

    Parameters:
        review_id

    Response:
        {user_id, tconst, rating, review_text}
    """
    review_id = request.args.get('review_id')
    result = reviews.get_review(review_id, g.db, g.cursor)
    return dumps(result)

@APP.route("/reviews/get-movie-reviews", methods=['GET'])
def get_movie_reviews():
    """
    Get all reviews of a given movie

    Parameters:
        tconst: tconst movie id to get reviews from
        user_id: the current user's id

    Response:
        [{review_id, user_id, tconst, rating, review_text}]
    """
    tconst = request.args.get('tconst')
    user_id = request.args.get('user_id')

    result = reviews.get_all_movie_reviews(tconst, user_id, g.db, g.cursor)
    return dumps(result)

@APP.route("/reviews/get-avg-movie-rating", methods=['GET'])
def get_avg_movie_rating():
    """
    Get the average user ratings of a movie

    Parameters:
        tconst: tconst movie id
        user_id: the current user's id

    Response:
        {average_rating}
    """
    tconst = request.args.get('tconst')
    user_id = request.args.get('user_id')

    result = reviews.get_average_movie_ratings_user(tconst, user_id, g.db, g.cursor)
    return dumps(result)

@APP.route("/reviews/update-review-text", methods=['PUT'])
def update_review_text():
    """
    Update the review text

    Parameters:
        review_id: the review id
        review_text: The new text to leave on the review

    Response:
        None
    """
    data = request.get_json()
    review_id = data['review_id']
    review_text = data['review_text']

    result = reviews.update_review_text(review_id, review_text, g.db, g.cursor)
    return dumps(result)

@APP.route("/reviews/delete-review", methods=['DELETE'])
def delete_review():
    """
    Delete a review given the review id. Only allows for deleting the
    user's own review

    Parameters:
        current_user_id
        review_id

    Response:
        None
    """
    data = request.get_json()
    current_user_id = data['current_user_id']
    review_id = data['review_id']

    result = reviews.delete_review(current_user_id, review_id, g.db, g.cursor)
    return dumps(result)

@APP.route("/admin/reviews/delete-review", methods=['DELETE'])
def delete_review_as_admin():
    """
    Delete a review as an admin. Admin can delete any review

    Parameters:
        current_user_id
        review_id

    Response:
        None
    """
    data = request.get_json()
    current_user_id = data['current_user_id']
    review_id = data['review_id']

    result = reviews.delete_review_as_admin(current_user_id, review_id, g.db, g.cursor)
    return dumps({})

@APP.route("/reviews/get-user-reviews", methods=["GET"])
def get_user_reviews():
    """
    Get all reviews made by a user

    Parameters:
        user_id

    Response:
        [{review_id, user_id, tconst, rating, review_text}]
    """
    user_id = request.args.get('user_id')

    result = reviews.get_user_reviews(user_id, g.db, g.cursor)
    return dumps(result)

@APP.route("/movie/get-imdb-tconst/<tmdb_movie_id>", methods=["GET"])
def get_imdb_tconst(tmdb_movie_id):
    """
    Get the tconst for a movie given the tmdb movie id

    Parameters:
        tmdb_movie_id (path param)

    Response:
        {tconst}
    """
    tconst = tmdb_api.get_imdb_tconst_from_tmdb_id(tmdb_movie_id)
    return dumps(tconst)

@APP.route("/movie/get-similar-movies/<tconst>", methods=["GET"])
def get_list_of_similar_movies(tconst):
    """
    Get a list of similar movies of given movie

    Parameters:
        tconst

    Response:
        {similar_movies}
    """
    similar_movies = tmdb_api.get_similar_movies(tconst)
    return dumps(similar_movies)

@APP.route("/movie/get-crew/<tconst>", methods=["GET"])
def get_movie_crew(tconst):
    """
    Get the crew memvers of a movie

    Parameters:
        tconst

    Response:
        [{nconst, role, character, name, birthYear}]
    """
    movie_crew = movie_details.get_movie_crew(tconst, g.db, g.cursor)
    return dumps(movie_crew)

@APP.route("/discussion/create", methods=["POST"])
def discussions_create():
    """
    Create a discussion forum

    Parameters:
        title: title of the forum
        description: descritpion of the forum post
        date: The date the forum post was made
    """
    data = request.get_json()
    title = data['title']
    description = data['description']
    date = data['date']
    status = forum.create_new_forum(title, description, date)
    return dumps(status)


@APP.route("/discussion/get-all-discussion-posts", methods=["GET"])
def get_all_discussions():
    """
    Get all discussion posts

    Parameters:
        None
    """
    movies = forum.get_movies_of_forum()
    return dumps(movies)

@APP.route("/discussion/get-discussion-post/<id>", methods=["GET"])
def get_forum_of_movie(id):
    """
    Get all discussion posts

    Parameters:
        id (path parameter): the id of a discussion post
    """
    discussion = forum.get_details_of_movie_forum(id)
    return dumps(discussion)

@APP.route("/discussion/comment/create", methods=["POST"])
def discussion_create_comment():
    """
    Create a comment on a discussion post

    Parameters:
        id (path parameter): the id of a discussion post
        comment: the comment to be added
        date: The date the comment was made
        user_id: the id of the user making the comment
    """
    data = request.get_json()
    title = data['id']
    comment = data['comment']
    date = data['datetime']
    user_id = data['user_id']
    res = forum.insert_comment(title, comment, date, user_id)
    return dumps({'is_success': res})

@APP.route("/discussion/comment/like", methods=["POST"])
def discussion_like_comment():
    """
    Like a comment on a discussion post
    
    Parameters:
        title: The title of the comment
        comment: The content of the comment
    """
    data = request.get_json()
    title = data['movie']
    comment = data['comment_id']
    res = forum.like_comment(title, comment)
    return dumps({'is_success': res})

@APP.route("/discussion/comment/delete", methods=["POST"])
def discussion_delete_comment():
    """
    Delete a comment on a discussion post
    
    Parameters:
        title: The title of the comment
        comment: The content of the comment
    """
    data = request.get_json()
    title = data['movie']
    comment = data['comment_id']
    print(comment)
    res = forum.delete_comment(title, comment)
    return dumps({'is_success': res})
    
@APP.route("/chatbot/get-query", methods=["POST"])
def get_chatbot_query():
    """
    Generates a response to a chatbot query
    
    Parameters:
        user_id: The user_id of the user
        user_query: The query from the chatbot input from the user
    """
    data = request.get_json()
    user_id = data["user_id"]
    user_query = data["user_query"]

    bot_query = chatbot.generate_query(user_id, g.db, g.cursor, user_query)

    return dumps(bot_query)

@APP.route("/admin/promote-user", methods=['POST'])
def promote_user_to_admin():
    """
    Promote a user to an admin. The user promoting
    the other use must also be an admin
    
    Parameters:
        user_to_promote: The user_id of the user to promote to admin
        current_user_id: The user_id of the current user trying to promote another user
    """
    data = request.get_json()
    user_to_promote = data["user_to_promote_id"]
    current_user_id = data["current_user_id"]

    admins.promote_another_user_as_admin(current_user_id, user_to_promote, g.db, g.cursor)
    return dumps({})

@APP.route("/admin/demote-user", methods=["POST"])
def demote_user_from_admin():
    """
    Demote a user from admin to a regular user. The user demoting another
    user must be an admin, and the user being demoted must also be an admin
    
    Parameters:
        user_to_demote: The user_id of the user to demote
        current_user_id: The user_id of the current user trying to demote another user
    """
    data = request.get_json()
    user_to_demote = data["user_to_demote_id"]
    current_user_id = data["current_user_id"]

    admins.demote_another_user_as_admin(current_user_id, user_to_demote, g.db, g.cursor)
    return dumps({})

@APP.route("/kids-mode/make-user-child-account", methods=["POST"])
def make_user_to_child_account():
    """
    Converts an existing account a child account. 
    
    Parameters:
        user_to_child_id: The user_id of the account to convert to a child account
    """
    data = request.get_json()
    # current_user_id = data["current_user_id"]
    user_to_child_id = data["user_to_child_id"]
    kids_friendly_mode.make_user_child_account(user_to_child_id, g.db, g.cursor)
    return dumps({})

@APP.route("/kids-mode/make-child-to-regular-account", methods=["POST"])
def make_child_to_regular_account():
    """
    Converts an existing child account a regular account. 
    
    Parameters:
        child_to_regular_account_id: The user_id of the account to convert to a regular account
    """
    data = request.get_json()
    # current_user_id = data["current_user_id"]
    child_to_regular_account_id = data["child_to_regular_account_id"]
    kids_friendly_mode.make_child_account_regular_account(child_to_regular_account_id, g.db, g.cursor)
    return dumps({})

if __name__ == "__main__":
    APP.run(port=5050)