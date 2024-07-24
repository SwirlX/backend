import wishlist
import pytest
import sqlite3

DB_PATH = "db/mydb.db"

@pytest.fixture(autouse=True)
def db_setup_and_teardown():
    # Setup phase
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Yield control to the test function
    yield conn, cur

    # Teardown phase
    cur.execute("DELETE FROM user_wishlist WHERE user_id LIKE 111111111")
    conn.commit()
    conn.close()

def test_wishlist_add(db_setup_and_teardown):
    conn, curr = db_setup_and_teardown
    
    user_id = 111111111
    tconst = 'tt0372784'
    
    # Add a movie to the wishlist
    curr_wishlist = wishlist.extract_wish_list_from_db(user_id, conn, curr)
    curr_wishlist = wishlist.add_to_wish_list(curr_wishlist, tconst)
    curr_wishlist = wishlist.convert_wish_list_to_db_form(curr_wishlist) 
    wishlist.insert_wish_list_into_db(user_id, curr_wishlist, conn, curr)
    # Extract the row that was added above
    rows = wishlist.extract_wish_list_from_db(user_id, conn, curr)
    # extract wishlist
    assert rows[0] == 'tt0372784'
    
    
def test_wishlist_add_more(db_setup_and_teardown):

    conn, curr = db_setup_and_teardown
    
    user_id = 111111111
    tconst = 'tt0372784'
    
    # Add a movie to the wishlist
    curr_wishlist = wishlist.extract_wish_list_from_db(user_id, conn, curr)
    curr_wishlist = wishlist.add_to_wish_list(curr_wishlist, tconst)
    curr_wishlist = wishlist.convert_wish_list_to_db_form(curr_wishlist) 
    wishlist.insert_wish_list_into_db(user_id, curr_wishlist, conn, curr)
    
    user_id = 111111111
    tconst = 'tt10327712'
    
    # Add a movie to the wishlist
    curr_wishlist = wishlist.extract_wish_list_from_db(user_id, conn, curr)
    curr_wishlist = wishlist.add_to_wish_list(curr_wishlist, tconst)
    curr_wishlist = wishlist.convert_wish_list_to_db_form(curr_wishlist) 
    wishlist.insert_wish_list_into_db(user_id, curr_wishlist, conn, curr)
    # Extract the row that was added above
    rows = wishlist.extract_wish_list_from_db(user_id, conn, curr)

    # extract wishlist 
    assert rows[0] == 'tt0372784'
    assert rows[1] == 'tt10327712'
    
def test_wishlist_remove(db_setup_and_teardown):
    
    conn, curr = db_setup_and_teardown
    user_id = 111111111
    current_wish_list = ['tt0372784', 'tt10327712']
    tconst = 'tt0372784'
    
    # Insert a wish list to remove from
    current_wish_list = wishlist.convert_wish_list_to_db_form(current_wish_list)
    wishlist.insert_wish_list_into_db(user_id, current_wish_list, conn, curr)
    # Perform the remove function
    curr_wishlist = wishlist.extract_wish_list_from_db(user_id, conn, curr)
    curr_wishlist = wishlist.remove_from_wish_list(curr_wishlist, tconst)
    curr_wishlist = wishlist.convert_wish_list_to_db_form(curr_wishlist) 
    wishlist.insert_wish_list_into_db(user_id, curr_wishlist, conn, curr)
    
    # Extract the row that was added above
    rows = wishlist.extract_wish_list_from_db(user_id, conn, curr)
    assert rows[0] == 'tt10327712'
    
def test_wishlist_remove_more(db_setup_and_teardown):
    conn, curr = db_setup_and_teardown
    user_id = 111111111
    current_wish_list = ['tt0372784', 'tt10327712']
    tconst = 'tt10327712'
    
    # Insert a wish list to remove from
    current_wish_list = wishlist.convert_wish_list_to_db_form(current_wish_list)
    wishlist.insert_wish_list_into_db(user_id, current_wish_list, conn, curr)
    # Perform the remove function
    curr_wishlist = wishlist.extract_wish_list_from_db(user_id, conn, curr)

    curr_wishlist = wishlist.remove_from_wish_list(curr_wishlist, tconst)
    curr_wishlist = wishlist.convert_wish_list_to_db_form(curr_wishlist) 
    wishlist.insert_wish_list_into_db(user_id, curr_wishlist, conn, curr)
    
    # Extract the row that was added above
    rows = wishlist.extract_wish_list_from_db(user_id, conn, curr)
    
    # Movie to remove
    tconst = 'tt0372784'
    # Perform the remove function
    curr_wishlist = wishlist.extract_wish_list_from_db(user_id, conn, curr)
    curr_wishlist = wishlist.remove_from_wish_list(curr_wishlist, tconst)
    curr_wishlist = wishlist.convert_wish_list_to_db_form(curr_wishlist) 
    wishlist.insert_wish_list_into_db(user_id, curr_wishlist, conn, curr)
    # Extract from db to verify that the wish list is empty.
    rows = wishlist.extract_wish_list_from_db(user_id, conn, curr)
    assert rows == ['']

def test_wishlist_view_wish_list(db_setup_and_teardown):
    
    conn, curr = db_setup_and_teardown
    user_id = 111111111
    # Batman Begins and Lego DC Batman
    current_wish_list = ['tt0372784', 'tt10327712']
    # Insert a wish list to extract from
    current_wish_list = wishlist.convert_wish_list_to_db_form(current_wish_list)
    wishlist.insert_wish_list_into_db(user_id, current_wish_list, conn, curr)
    
    rows = wishlist.extract_wish_list_from_db(user_id, conn, curr)
    view_wish_list = wishlist.show_wish_list_movie_data(rows, conn, curr)
    returned_data_list = view_wish_list["wishlist"]  
    
    assert returned_data_list == [{'tconst': 'tt0372784', 'primaryTitle': 'Batman Begins', 'startYear': 2005, 'genres': 'Action,Crime,Drama', 'averageRating': 8.2}, 
                                  {'tconst': 'tt10327712', 'primaryTitle': 'Lego DC Batman: Family Matters', 'startYear': 2019, 'genres': 'Action,Animation,Comedy', 'averageRating': 6.1}]