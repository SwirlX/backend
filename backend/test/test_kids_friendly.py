import auth
import pytest
import sqlite3
import admins
import error
import kids_friendly_mode

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

@pytest.fixture(autouse=True)
def register_user(db_setup_and_teardown):
    conn, cur = db_setup_and_teardown
    user_dict = auth.register_user("testingjohnsmith@email.com", "fakepassword", "john", "smith", "09/11/2001", 23, conn, cur)
    yield user_dict["user_id"]


def test_register_child_aged_account(db_setup_and_teardown):
    conn, cur = db_setup_and_teardown

    user_dict = auth.register_user("testingchildacc@email.com", "fakepassword", "timmy", "time", "2018-04-04T06:55:15.126Z", 5, conn, cur)

    user_id = user_dict["user_id"]

    is_user_child = kids_friendly_mode.is_user_child(user_id, conn, cur)

    assert is_user_child

def test_register_non_child_aged_account(db_setup_and_teardown):
    conn, cur = db_setup_and_teardown

    user_dict = auth.register_user("testingchildacc@email.com", "fakepassword", "timmy", "time", "2000-04-04T06:55:15.126Z", 23, conn, cur)

    user_id = user_dict["user_id"]

    is_user_child = kids_friendly_mode.is_user_child(user_id, conn, cur)

    assert not is_user_child
