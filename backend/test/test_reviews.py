import reviews
import pytest
import sqlite3
import error
from server import APP
import auth
import admins
import banlist

DB_PATH = "db/mydb.db"

@pytest.fixture(autouse=True)
def db_setup_and_teardown():
    # Setup phase
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Yield control to the test function
    yield conn, cur

    # Teardown phase
    cur.execute("DELETE FROM reviews WHERE review_text LIKE '%testing%'")
    cur.execute("DELETE FROM users WHERE email LIKE '%testing%'")
    conn.commit()
    conn.close()

# Create fixture that registers a user
@pytest.fixture(autouse=True)
def register_user(db_setup_and_teardown):
    conn, cur = db_setup_and_teardown
    user_dict = auth.register_user("testingjohnsmith@email.com", "fakepassword", "john", "smith", "09/11/2001", "22", conn, cur)
    yield user_dict["user_id"]

# Create fixture that registers a 2nd user
@pytest.fixture()
def register_2nd_user(db_setup_and_teardown):
    conn, cur = db_setup_and_teardown
    user_dict = auth.register_user("testingpeterapple@email.com", "fakepassword", "peter", "apple", "10/11/2001", "22", conn, cur)
    yield user_dict["user_id"]
    

def test_review_creation(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user

    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    cur.execute("SELECT user_id, tconst, rating, review_text FROM reviews WHERE review_text = 'testing review 123'")
    review_dict = cur.fetchone()

    assert review_dict[0] == user_id
    assert review_dict[1] == 'tt0000001'
    assert review_dict[2] == 4.12
    assert review_dict[3] == 'testing review 123'

def test_review_creation_failure_user_doesnt_exist(db_setup_and_teardown):
    conn, cur = db_setup_and_teardown

    with pytest.raises(error.InputError):
        reviews.create_review("-1", "tt0000001", "4.12", "testing review 123", conn, cur)

def test_review_creation_failure_movie_doesnt_exist(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user

    with pytest.raises(error.DatabaseError):
        reviews.create_review(register_user, "-1", "4.12", "testing review 123", conn, cur)

def test_get_review_id(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user

    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    review_id = reviews.get_review_id(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    assert review_id is not None
    assert review_id > 0

def test_get_review_id_not_found(db_setup_and_teardown, register_user):
    # Test exception is raised if review_id is not found
    conn, cur = db_setup_and_teardown
    user_id = register_user

    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    with pytest.raises(error.InputError):
        reviews.get_review_id("-1", "tt0000001", "4.12", "testing review 123", conn, cur)

def test_getting_a_review(db_setup_and_teardown, register_user):
    # Test getting a review given a review_id
    conn, cur = db_setup_and_teardown
    user_id = register_user

    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 456", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 789", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 1011", conn, cur)

    review_id = reviews.get_review_id(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    review = reviews.get_review(review_id, conn, cur)
    
    assert review is not None
    assert review["user_id"] == user_id
    assert review["tconst"] == "tt0000001"
    assert review["rating"] == 4.12
    assert review["review_text"] == "testing review 123"

def testing_getting_a_review_not_found(db_setup_and_teardown, register_user):
    # Test exception is raised if review_id is not found
    conn, cur = db_setup_and_teardown
    user_id = register_user

    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 456", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 789", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 1011", conn, cur)


    with pytest.raises(error.DatabaseError):
        review = reviews.get_review(-1, conn, cur)



def test_getting_all_movie_reviews(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user


    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 456", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 789", conn, cur)

    all_reviews = reviews.get_all_movie_reviews("tt0000001", user_id, conn, cur)

    reviews_list = all_reviews["reviews"]
    assert len(reviews_list) == 3
    assert reviews_list[0]["user_id"] == user_id
    assert reviews_list[0]["tconst"] == "tt0000001"
    assert reviews_list[0]["rating"] == 4.12
    assert reviews_list[0]["review_text"] == "testing review 123"
    assert reviews_list[1]["user_id"] == user_id
    assert reviews_list[1]["tconst"] == "tt0000001"
    assert reviews_list[1]["rating"] == 4.12
    assert reviews_list[1]["review_text"] == "testing review 456"
    assert reviews_list[2]["user_id"] == user_id
    assert reviews_list[2]["tconst"] == "tt0000001"
    assert reviews_list[2]["rating"] == 4.12
    assert reviews_list[2]["review_text"] == "testing review 789"

def test_get_all_reviews_but_banlist_user_reviews(db_setup_and_teardown, register_user, register_2nd_user):

    conn, curr = db_setup_and_teardown
    
    user_id = register_user
    user_id_2 = register_2nd_user
    
    review_1_id = reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, curr)
    review_2_id = reviews.create_review(user_id_2, "tt0000001", "4.12", "testing review 456", conn, curr)
    
    
    curr_banlist = str(user_id_2)
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)

    all_reviews = reviews.get_all_movie_reviews("tt0000001", user_id, conn, curr)

    reviews_list = all_reviews["reviews"]
    
    assert len(reviews_list) == 1
    assert reviews_list[0]["user_id"] == user_id
    assert reviews_list[0]["tconst"] == "tt0000001"
    assert reviews_list[0]["rating"] == 4.12
    assert reviews_list[0]["review_text"] == "testing review 123"
    
def test_get_all_reviews_admin_user(db_setup_and_teardown, register_user, register_2nd_user):
    
    conn, curr = db_setup_and_teardown
    
    user_id = register_user
    admins.make_user_admin(user_id, conn, curr)
    user_id_2 = register_2nd_user
    
    review_1_id = reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, curr)
    review_2_id = reviews.create_review(user_id_2, "tt0000001", "4.12", "testing review 456", conn, curr)
    
    
    curr_banlist = str(user_id_2)
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)

    all_reviews = reviews.get_all_movie_reviews("tt0000001", user_id, conn, curr)

    reviews_list = all_reviews["reviews"]
    
    assert len(reviews_list) == 2
    assert reviews_list[0]["user_id"] == user_id
    assert reviews_list[0]["tconst"] == "tt0000001"
    assert reviews_list[0]["rating"] == 4.12
    assert reviews_list[0]["review_text"] == "testing review 123"
    assert reviews_list[1]["user_id"] == user_id_2
    assert reviews_list[1]["tconst"] == "tt0000001"
    assert reviews_list[1]["rating"] == 4.12
    assert reviews_list[1]["review_text"] == "testing review 456"
    
def test_updating_review_text(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user

    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 456", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 789", conn, cur)

    review_id = reviews.get_review_id(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    reviews.update_review_text(review_id, "testing new review 999", conn, cur)
    review_id = reviews.get_review_id(user_id, "tt0000001", "4.12", "testing new review 999", conn, cur)

    review = reviews.get_review(review_id, conn, cur)

    assert review["review_text"] == "testing new review 999"
    assert review["rating"] == 4.12
    assert review["tconst"] == "tt0000001"
    assert review["user_id"] == user_id

def test_updating_review_text_failed(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user

    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)
    
    with pytest.raises(error.DatabaseError):
        reviews.update_review_text(-1, "testing new review 999", conn, cur)


def test_deleting_review(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user

    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    review_id = reviews.get_review_id(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    reviews.delete_review(user_id, review_id, conn, cur)

    with pytest.raises(error.DatabaseError):
        reviews.get_review(review_id, conn, cur)

def test_deleting_review_that_doesnt_exist(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user

    with pytest.raises(error.DatabaseError):
        reviews.delete_review(user_id ,-1, conn, cur)

def test_deleting_review_then_updating(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user

    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    review_id = reviews.get_review_id(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    reviews.delete_review(user_id, review_id, conn, cur)

    with pytest.raises(error.DatabaseError):
        reviews.update_review_text(review_id, "testing new review 999", conn, cur)

def test_deleting_another_users_review(db_setup_and_teardown, register_user, register_2nd_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user
    another_user_id = register_2nd_user

    reviews.create_review(another_user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    review_id = reviews.get_review_id(another_user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    with pytest.raises(error.AccessError):
        reviews.delete_review(user_id, review_id, conn, cur)

def test_deleting_another_users_review_as_admin(db_setup_and_teardown, register_user, register_2nd_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user
    another_user_id = register_2nd_user

    reviews.create_review(another_user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    review_id = reviews.get_review_id(another_user_id, "tt0000001", "4.12", "testing review 123", conn, cur)

    admins.make_user_admin(user_id, conn, cur)

    reviews.delete_review_as_admin(user_id, review_id, conn, cur)

    # Verify the review is deleted by checking that it raises an error when retrieving
    with pytest.raises(error.DatabaseError):
        reviews.get_review(review_id, conn, cur)


def test_getting_all_user_reviews(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user

    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 123", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 456", conn, cur)
    reviews.create_review(user_id, "tt0000001", "4.12", "testing review 789", conn, cur)
    reviews.create_review(user_id, "tt0000002", "3.50", "testing review of movie 2", conn, cur)

    all_reviews = reviews.get_user_reviews(user_id, conn, cur)

    reviews_list = all_reviews["reviews"]
    assert len(reviews_list) == 4
    assert reviews_list[0]["user_id"] == user_id
    assert reviews_list[0]["tconst"] == "tt0000001"
    assert reviews_list[0]["rating"] == 4.12
    assert reviews_list[0]["review_text"] == "testing review 123"
    assert reviews_list[1]["user_id"] == user_id
    assert reviews_list[1]["tconst"] == "tt0000001"
    assert reviews_list[1]["rating"] == 4.12
    assert reviews_list[1]["review_text"] == "testing review 456"
    assert reviews_list[2]["user_id"] == user_id
    assert reviews_list[2]["tconst"] == "tt0000001"
    assert reviews_list[2]["rating"] == 4.12
    assert reviews_list[2]["review_text"] == "testing review 789"
    assert reviews_list[3]["user_id"] == user_id
    assert reviews_list[3]["tconst"] == "tt0000002"
    assert reviews_list[3]["rating"] == 3.50
    assert reviews_list[3]["review_text"] == "testing review of movie 2"

def test_getting_all_user_reviews_failed(db_setup_and_teardown, register_user):
    conn, cur = db_setup_and_teardown
    user_id = register_user

    with pytest.raises(error.InputError):
        reviews.get_user_reviews(-1, conn, cur)
        
def test_get_all_average_movie_ratings_with_banlist(db_setup_and_teardown, register_user, register_2nd_user):
    
    conn, curr = db_setup_and_teardown
    
    user_id = register_user
    user_id_2 = register_2nd_user
    
    review_1_id = reviews.create_review(user_id, "tt0000001", "1", "testing review 123", conn, curr)
    review_2_id = reviews.create_review(user_id_2, "tt0000001", "4", "testing review 456", conn, curr)
    review_3_id = reviews.create_review(user_id, "tt0000001", "6", "testing review 789", conn, curr)

    
    curr_banlist = str(user_id_2)
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)

    all_reviews = reviews.get_average_movie_ratings_user("tt0000001", user_id, conn, curr)

    average_rating = all_reviews["average_rating"]
    
    assert average_rating == 3.5
    
def test_get_all_average_movie_ratings_1(db_setup_and_teardown, register_user, register_2nd_user):
    
    conn, curr = db_setup_and_teardown
    
    user_id = register_user
    user_id_2 = register_2nd_user
    
    review_1_id = reviews.create_review(user_id, "tt0000001", "0", "testing review 123", conn, curr)
    review_2_id = reviews.create_review(user_id_2, "tt0000001", "5", "testing review 456", conn, curr)
    
    all_reviews = reviews.get_average_movie_ratings_user("tt0000001", user_id, conn, curr)

    average_rating = all_reviews["average_rating"]
    
    assert average_rating == 2.5
    
def test_get_all_average_movie_ratings_2(db_setup_and_teardown, register_user, register_2nd_user):
    
    conn, curr = db_setup_and_teardown
    
    user_id = register_user
    user_id_2 = register_2nd_user
    
    review_1_id = reviews.create_review(user_id, "tt0000001", "3.14", "testing review 123", conn, curr)
    review_2_id = reviews.create_review(user_id_2, "tt0000001", "4.20", "testing review 456", conn, curr)
    
    all_reviews = reviews.get_average_movie_ratings_user("tt0000001", user_id, conn, curr)

    average_rating = all_reviews["average_rating"]
    
    assert average_rating == 3.7
    
def test_get_all_average_movie_ratings_3(db_setup_and_teardown, register_user, register_2nd_user):
    
    conn, curr = db_setup_and_teardown
    
    user_id = register_user
    user_id_2 = register_2nd_user
    
    reviews.create_review(user_id, "tt0000001", "3.14", "testing review 123", conn, curr)
    reviews.create_review(user_id, "tt0000001", "4.20", "testing review 456", conn, curr)
    reviews.create_review(user_id, "tt0000001", "5.60", "testing review 789", conn, curr)
    
    all_reviews = reviews.get_average_movie_ratings_user("tt0000001", user_id, conn, curr)

    average_rating = all_reviews["average_rating"]
    
    assert average_rating == 4.3