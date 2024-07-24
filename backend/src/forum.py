import data
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random

client = MongoClient(data.MONGODB_KEY, server_api=ServerApi('1'))

def check_if_db_exists():
    """
    Checks whether a DB exists 
    If not, create one

    Parameters:
        None

    Returns:
        A database
    """
    dblist = client.list_database_names()
    if "Forums" not in dblist:
        db = client.Forums
        return db

def get_movies_of_forum():
    """
        Get movies that are in the forum

    Parameters:
        None

    Returns:
        list of movies that are in the forum
    """
    collist = client.Forum.list_collection_names()
    return collist

def get_details_of_movie_forum(movie):
    """
    Gets comments of a forum

    Parameters:
        movie: movie which comments are being retrieved from

    Returns:
        All comments for a particular movie
    """
    comments = client.Forum[movie].find_one()
    return comments

def create_new_forum(movie, description, date):
    """
    Creates new forum

    Parameters:
        Movie: the movie the forum is being created about
        Description: a description of the forum
        Date: the date the forum was created

    Returns:
        boolean value
        True if forum is successfully created
        False otherwise
    """
    col = client.Forum[movie]
    try:
        #MongoDB collection is not created until there is content
        col.insert_one({
            '_id': movie,
            'description': description,
            'date': date,
            'comments': []
        })
        return True
    except:
        return False

def insert_comment(movie, comment, date, user_id):
    """
    Adds new comment to forum

    Parameters:
        movie: movie which comments are being inserted to
        comment: the users comment
        date: the date the comment is made
        user_id: the users id

    Returns:
        boolean value
        True if comment is successfully created
        False otherwise
    """
    cursor = "Needs to be empty"
    while (cursor != None):
        rand = random.random()
        col = client.Forum[movie]
        cursor = col.find_one({
            "comments" : { "$elemMatch": {
                    "_id": rand,
                }
            }
        })
    
    try:
        col.update_one(
            {"_id": movie},
            {"$addToSet": { "comments": 
                {
                    "date": date,
                    "comment": comment,
                    "likes": 0,
                    "user_id": user_id,
                    "_id": rand
                }
            }})
        return True
    except:
        return False

def delete_comment(movie, comment_id):
    """
    Deletes comment from a forum

    Parameters:
        movie: movie which comment is being deleted from
        comment_id: id of the comment being deleted

    Returns:
        boolean value
        True if comment is successfully deleted
        False otherwise
    """
    col = client.Forum[movie]
    try:
        cursor = list(col.update_many({'_id': movie}, {'$pull': {
            'comments': {'_id': comment_id}} ,
        }))
        print(cursor)
        return True 
    except:
        return False
    
    
def like_comment(movie, id):
    """
    Updates the likes in a comment

    Parameters:
        movie: tconst of movie which like is being updated for
        id: id of comment which is being updated

    Returns:
        boolean value
        True if likes are successfully updated
        False otherwise
    """
    col = client.Forum[movie]
    likes = 1
    print(id)
    comment = list(col.find())
    commentList = comment[0]["comments"]
    for comment in commentList:
        if comment['_id'] == id:
            likes = comment["likes"] + 1
            break

    try:
        col.update_one({'_id': movie, 'comments._id': id}, {'$set': {
            'comments.$.likes': likes} ,
        })
        return True
    except:
        return False
