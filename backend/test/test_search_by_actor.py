import search
import pytest
import sqlite3
import auth

DB_PATH = "db/mydb.db"

@pytest.fixture(autouse=True)
def db_setup_and_teardown():
    # Setup phase
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Yield control to the test function
    yield conn, cur

    # Teardown phase
    cur.execute("DELETE FROM users WHERE email LIKE '%testing%'")
    conn.commit()
    conn.close()

# Create fixture that registers a user
@pytest.fixture(autouse=True)
def register_user(db_setup_and_teardown):
    conn, cur = db_setup_and_teardown
    user_dict = auth.register_user("testingjohnsmith@email.com", "fakepassword", "john", "smith", "09/11/2001", "22", conn, cur)
    yield user_dict["user_id"]

def test_search_christian_bale(db_setup_and_teardown, register_user):
    '''
    Test to see whether a generic search will work with all lower case characters.
    '''
    conn, cursor = db_setup_and_teardown
    user_id = register_user

    search_results_list = search.search_by_actor(user_id, "christian bale", conn, cursor)

    
    #print(search_results_list)
    
    assert search_results_list == {'movies': [{'tconst': 'tt0964517', 'primaryTitle': 'The Fighter', 'year': 2010, 'genres': 'Action,Biography,Drama', 'rating': 7.8, 'poster_image': 'https://image.tmdb.org/t/p/w500/gmTLorYhXJZgdzUsUhvm1ZkRTl0.jpg'}, 
                                              {'tconst': 'tt0468569', 'primaryTitle': 'The Dark Knight', 'year': 2008, 'genres': 'Action,Crime,Drama', 'rating': 9, 'poster_image': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg'}, 
                                              {'tconst': 'tt0144084', 'primaryTitle': 'American Psycho', 'year': 2000, 'genres': 'Crime,Drama,Horror', 'rating': 7.6, 'poster_image': 'https://image.tmdb.org/t/p/w500/9uGHEgsiUXjCNq8wdq4r49YL8A1.jpg'}, 
                                              {'tconst': 'tt0372784', 'primaryTitle': 'Batman Begins', 'year': 2005, 'genres': 'Action,Crime,Drama', 'rating': 8.2, 'poster_image': 'https://image.tmdb.org/t/p/w500/4MpN4kIEqUjW8OPtOQJXlTdHiJV.jpg'}]}


def test_search_Christian_Bale_2(db_setup_and_teardown, register_user):
    '''
    Test to differentiate between using lower case and upper case for the search field.
    '''
    conn, cursor = db_setup_and_teardown
    user_id = register_user
    search_results_list = search.search_by_actor(user_id, "Christian Bale", conn, cursor)

    
    print(search_results_list)
    
    assert search_results_list == {'movies': [{'tconst': 'tt0964517', 'primaryTitle': 'The Fighter', 'year': 2010, 'genres': 'Action,Biography,Drama', 'rating': 7.8, 'poster_image': 'https://image.tmdb.org/t/p/w500/gmTLorYhXJZgdzUsUhvm1ZkRTl0.jpg'}, 
                                              {'tconst': 'tt0468569', 'primaryTitle': 'The Dark Knight', 'year': 2008, 'genres': 'Action,Crime,Drama', 'rating': 9, 'poster_image': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg'}, 
                                              {'tconst': 'tt0144084', 'primaryTitle': 'American Psycho', 'year': 2000, 'genres': 'Crime,Drama,Horror', 'rating': 7.6, 'poster_image': 'https://image.tmdb.org/t/p/w500/9uGHEgsiUXjCNq8wdq4r49YL8A1.jpg'}, 
                                              {'tconst': 'tt0372784', 'primaryTitle': 'Batman Begins', 'year': 2005, 'genres': 'Action,Crime,Drama', 'rating': 8.2, 'poster_image': 'https://image.tmdb.org/t/p/w500/4MpN4kIEqUjW8OPtOQJXlTdHiJV.jpg'}]}


def test_search_morgan_freeman(db_setup_and_teardown, register_user):
    '''
    Test to see whether a generic search will work with all upper case characters.
    '''
    conn, cursor = db_setup_and_teardown
    user_id = register_user
    
    search_results_list = search.search_by_actor(user_id, "MORGAN FREEMAN", conn, cursor)

    
    print(search_results_list)
    
    assert search_results_list == {'movies': [{'tconst': 'tt0468569', 'primaryTitle': 'The Dark Knight', 'year': 2008, 'genres': 'Action,Crime,Drama', 'rating': 9, 'poster_image': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg'}, 
                                              {'tconst': 'tt1057500', 'primaryTitle': 'Invictus', 'year': 2009, 'genres': 'Action,Biography,Drama', 'rating': 7.3, 'poster_image': 'https://image.tmdb.org/t/p/w500/cNUoXM8dtg5mRt90GLrAHBP9IGE.jpg'}, 
                                              {'tconst': 'tt0097239', 'primaryTitle': 'Driving Miss Daisy', 'year': 1989, 'genres': 'Comedy,Drama,Romance', 'rating': 7.3, 'poster_image': 'https://image.tmdb.org/t/p/w500/iaCzvcY42HihFxQBTZCTKMpsI0P.jpg'}, 
                                              {'tconst': 'tt0114369', 'primaryTitle': 'Se7en', 'year': 1995, 'genres': 'Crime,Drama,Mystery', 'rating': 8.6, 'poster_image': 'https://image.tmdb.org/t/p/w500/6yoghtyTpznpBik8EngEmJskVUO.jpg'}]}

def test_search_non_existent_actor(db_setup_and_teardown, register_user): 
    '''
    Test search by actor for a non-existent actor.
    '''
    conn, cursor = db_setup_and_teardown
    user_id = register_user

    search_results_list = search.search_by_actor(user_id, "XDGXVXD", conn, cursor)

    
    print(search_results_list)
    
    assert search_results_list == {'movies': []}