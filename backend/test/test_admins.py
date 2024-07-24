import auth
import pytest
import sqlite3
import admins
import error

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
    user_dict = auth.register_user("testingjohnsmith@email.com", "fakepassword", "john", "smith", "09/11/2001", "22", conn, cur)
    yield user_dict["user_id"]

# Create fixture that registers a 2nd user
@pytest.fixture()
def register_2nd_user(db_setup_and_teardown):
    conn, cur = db_setup_and_teardown
    user_dict = auth.register_user("testingpeterapple@email.com", "fakepassword", "peter", "apple", "10/11/2001", "22", conn, cur)
    yield user_dict["user_id"]

def test_make_user_admin(db_setup_and_teardown, register_user):
    # Unpack the fixture values
    conn, cur = db_setup_and_teardown
    user_id = register_user

    res_cur = cur.execute("SELECT is_admin FROM users WHERE user_id=?", (user_id,))
    is_admin_old = res_cur.fetchone()[0]

    # Test
    admins.make_user_admin(user_id, conn, cur)

    # Verify
    res_cur = cur.execute("SELECT is_admin FROM users WHERE user_id=?", (user_id,))
    is_admin = res_cur.fetchone()[0]

    assert is_admin_old == 0
    assert is_admin == 1

def test_admin_demotion(db_setup_and_teardown, register_user):
    # Unpack the fixture values
    conn, cur = db_setup_and_teardown
    user_id = register_user

    old_is_admin = admins.user_is_admin(user_id, conn, cur)
    admins.make_user_admin(user_id, conn, cur)
    is_admin = admins.user_is_admin(user_id, conn, cur)
    assert is_admin == 1

    admins.demote_admin(user_id, conn, cur)
    new_is_admin = admins.user_is_admin(user_id, conn, cur)
    assert new_is_admin == 0


def test_make_user_admin_when_already_admin(db_setup_and_teardown, register_user):
    # Unpack the fixture values
    conn, cur = db_setup_and_teardown
    user_id = register_user

    res_cur = cur.execute("SELECT is_admin FROM users WHERE user_id=?", (user_id,))
    is_admin_old = res_cur.fetchone()[0]

    # Test
    admins.make_user_admin(user_id, conn, cur)

    with pytest.raises(error.InputError):
        admins.make_user_admin(user_id, conn, cur)
