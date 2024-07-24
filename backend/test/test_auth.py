import auth
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
    cur.execute("DELETE FROM users WHERE email LIKE '%testing%'")
    conn.commit()
    conn.close()

def test_auth_register(db_setup_and_teardown):
    # Unpack the fixture values
    conn, cur = db_setup_and_teardown

    # Test phase
    user_dict = auth.register_user("testingjohnsmith@email.com", "fakepassword", "john", "smith", "09/11/2001", "22", conn, cur)

    print("User ID is " + str(user_dict["user_id"]))
    user_id = user_dict["user_id"]

    cur.execute("SELECT * FROM users WHERE user_id =?", (user_id,))
    user = cur.fetchone()

    # columns: user_id | first_name | last_name | email | password| dob | token

    assert user is not None
    assert user[0] == user_id
    assert user[1] == "john"
    assert user[2] == "smith"
    assert user[3] == "testingjohnsmith@email.com"
    # assert user[4] is password
    assert user[5] == "09/11/2001"
    assert user[6] == user_dict["token"]

def test_auth_logout(db_setup_and_teardown):
    # Setup phase
    conn, cur = db_setup_and_teardown
    user_dict = auth.register_user("testingjohnsmith@email.com", "fakepassword", "john", "smith", "09/11/2001", "22", conn, cur)

    user_id = user_dict["user_id"]
    token = user_dict["token"]

    cur.execute("SELECT token FROM users WHERE user_id =?", (user_id,))
    stored_token = cur.fetchone()[0]
    assert stored_token == token

    response = auth.logout_user(token, conn, cur)
    cur.execute("SELECT token FROM users WHERE user_id =?", (user_id,))
    new_token = cur.fetchone()[0]
    assert new_token is None
    assert response["is_success"] is True

def test_auth_login(db_setup_and_teardown):
    # Setup phase (Register user)
    conn, cur = db_setup_and_teardown
    user_dict = auth.register_user("testingjohnsmith@email.com", "fakepassword", "john", "smith", "09/11/2001", "22", conn, cur)

    user_id = user_dict["user_id"]
    old_token = user_dict["token"]

    cur.execute("SELECT token FROM users WHERE user_id =?", (user_id,))
    stored_token = cur.fetchone()[0]
    assert stored_token == old_token

    # ---- Log the user out to ensure token is set to NULL ----
    response = auth.logout_user(old_token, conn, cur)
    assert response["is_success"] is True

    # ---- Log the user back in to ensure token is set properly ----
    user_dict = auth.login_user("testingjohnsmith@email.com", "fakepassword", conn, cur)
    user_id = user_dict["user_id"]
    new_token = user_dict["token"]

    cur.execute("SELECT token FROM users WHERE user_id =?", (user_id,))
    newly_stored_token = cur.fetchone()[0]
    assert new_token is not None
    assert new_token == newly_stored_token



