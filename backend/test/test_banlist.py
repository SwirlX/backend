from unittest.case import _AssertRaisesContext
import banlist
import pytest
import sqlite3
import error

DB_PATH = "db/imdb.db"

@pytest.fixture(autouse=True)
def db_setup_and_teardown():
    # Setup phase
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Yield control to the test function
    yield conn, cur

    # Teardown phase
    cur.execute("DELETE FROM user_banlist WHERE user_id LIKE 1")
    conn.commit()
    conn.close()

def test_insert_banlist(db_setup_and_teardown):
    '''
    This test ensures that the insert_banlist_into_db functionality works as required.
    '''
    conn, curr = db_setup_and_teardown
    
    user_id = 1
    curr_banlist = '2,3,4,5'
    
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    result_banlist = banlist.extract_banlist_from_db(user_id, conn, curr)
    
    assert result_banlist == ['2', '3', '4', '5']

def test_extract_banlist(db_setup_and_teardown):
    '''
    This test ensures that the extract_banlist_from_db functionality works as required.
    '''
    conn, curr = db_setup_and_teardown
    
    user_id_1 = 1
    curr_banlist_1 = '2,3,4,5'
    banlist.insert_banlist_into_db(user_id_1, curr_banlist_1, conn, curr)
    
    user_id_2 = 2
    curr_banlist_2 = '7,8,9,10'
    banlist.insert_banlist_into_db(user_id_2, curr_banlist_2, conn, curr)
    
    test_result_1 = banlist.extract_banlist_from_db(user_id_1, conn, curr)
    test_result_2 = banlist.extract_banlist_from_db(user_id_2, conn, curr)

    assert test_result_1 == ['2', '3', '4', '5']
    assert test_result_2 == ['7', '8', '9', '10']    
    
    curr.execute("DELETE FROM user_banlist WHERE user_id LIKE 2")
    
def test_add_to_banlist(db_setup_and_teardown):
    '''
    This test ensures tha the add_user_to_banlist functionality works as required.
    '''
    conn, curr = db_setup_and_teardown
    
    user_id = 1
    curr_banlist = '2,3,4,5'
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    
    user_id_to_ban = 8
    # Add user to the banlist
    curr_banlist = banlist.extract_banlist_from_db(user_id, conn, curr)
    curr_banlist = banlist.add_user_to_banlist(curr_banlist, user_id_to_ban)
    print(41)
    print(curr_banlist)
    print(type(curr_banlist))
    curr_banlist = banlist.convert_banlist_to_db_form(curr_banlist)
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    
    rows = banlist.extract_banlist_from_db(user_id, conn, curr)
    print(rows)
    
    assert rows == ['2', '3', '4', '5', '8']
    
    
def test_remove_from_banlist(db_setup_and_teardown):
    conn, curr = db_setup_and_teardown
    
    user_id = 1
    curr_banlist = '2,3,4,5'
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    
    user_id_to_remove = 3
    # Add user to the banlist
    curr_banlist = banlist.extract_banlist_from_db(user_id, conn, curr)
    curr_banlist = banlist.remove_user_from_banlist(curr_banlist, user_id_to_remove)
    print(41)
    print(curr_banlist)
    print(type(curr_banlist))
    curr_banlist = banlist.convert_banlist_to_db_form(curr_banlist)
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    
    rows = banlist.extract_banlist_from_db(user_id, conn, curr)
    print(rows)
    
    assert rows == ['2', '4', '5']
    
# def test_adding_currently_existing_user_in_banlist(db_setup_and_teardown):
#     conn, curr = db_setup_and_teardown
    
#     user_id = 1
#     curr_banlist = '2,3,4,5'
#     banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    
#     user_id_to_ban = 4
#     # Add user to the banlist
#     curr_banlist = banlist.extract_banlist_from_db(user_id, conn, curr)
#     curr_banlist = banlist.add_user_to_banlist(curr_banlist, user_id_to_ban)
#     curr_banlist = banlist.convert_banlist_to_db_form(curr_banlist)
#     banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    
#     rows = banlist.extract_banlist_from_db(user_id, conn, curr)
#     print(rows)
    
# def test_removing_user_not_in_banlist(db_setup_and_teardown):
    
#     conn, curr = db_setup_and_teardown
    
#     user_id = 2
#     curr_banlist = None
#     banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    
#     user_id_to_remove = 7
#     # Add user to the banlist
#     curr_banlist = banlist.extract_banlist_from_db(user_id, conn, curr)
#     curr_banlist = banlist.remove_user_from_banlist(curr_banlist, user_id_to_remove)
#     print(41)
#     print(curr_banlist)
#     print(type(curr_banlist))
#     curr_banlist = banlist.convert_banlist_to_db_form(curr_banlist)
#     banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    
#     rows = banlist.extract_banlist_from_db(user_id, conn, curr)
#     print(rows)
    
#     assert 1 == 2
    
def test_remove_all_from_banlist(db_setup_and_teardown):
    conn, curr = db_setup_and_teardown
    
    user_id = 1
    curr_banlist = '2,3'
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    
    user_id_to_remove = 2
    # Add user to the banlist
    curr_banlist = banlist.extract_banlist_from_db(user_id, conn, curr)
    curr_banlist = banlist.remove_user_from_banlist(curr_banlist, user_id_to_remove)
    curr_banlist = banlist.convert_banlist_to_db_form(curr_banlist)
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    user_id_to_remove = 3
    curr_banlist = banlist.extract_banlist_from_db(user_id, conn, curr)
    curr_banlist = banlist.remove_user_from_banlist(curr_banlist, user_id_to_remove)
    curr_banlist = banlist.convert_banlist_to_db_form(curr_banlist)
    banlist.insert_banlist_into_db(user_id, curr_banlist, conn, curr)
    
    rows = banlist.extract_banlist_from_db(user_id, conn, curr)
    print(rows)
    
    assert rows == ['']
    
    
def test_get_user_details(db_setup_and_teardown):
    conn, curr = db_setup_and_teardown
    
    result = banlist.get_banlist_user_details(['1', '2', '3'], conn, curr)
    print(result)
    
    assert result == {'banlist_user_details': [{'user_id': 1, 'first_name': 'John', 'last_name': 'Smith', 'email': 'email1'}, 
                                               {'user_id': 2, 'first_name': 'Batman', 'last_name': 'Batman', 'email': 'batman'}, 
                                               {'user_id': 3, 'first_name': 'Bruce', 'last_name': 'Wayne', 'email': 'brucewayne'}]}