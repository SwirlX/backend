import search
import pytest
import sqlite3

DB_PATH = "db/mydb.db"

def test_search_theMatrix():
    conn = sqlite3.connect("db/mydb.db")
    cursor = conn.cursor()
    search_results_list = search.search_movie("the matrix", conn, cursor)

    assert search_results_list != []
    assert search_results_list[0] == ('tt0234215', 'The Matrix Reloaded', '2003', 'Action,Sci-Fi', '7.2')
    assert search_results_list[1] == ('tt0242653', 'The Matrix Revolutions', '2003', 'Action,Sci-Fi', '6.7')

def test_search_batman():

    conn = sqlite3.connect("db/mydb.db")
    cursor = conn.cursor()
    search_results_list = search.search_movie("batman", conn, cursor)

    assert search_results_list == [('tt0096895', 'Batman', '1989', 'Action,Adventure', '7.5'), 
                                    ('tt0103776', 'Batman Returns', '1992', 'Action,Crime,Fantasy', '7.1'), 
                                    ('tt0106364', 'Batman: Mask of the Phantasm', '1993', 'Action,Adventure,Animation', '7.8'), 
                                    ('tt0112462', 'Batman Forever', '1995', 'Action,Adventure', '5.4'), 
                                    ('tt0118688', 'Batman & Robin', '1997', 'Action,Sci-Fi', '3.7'), 
                                    ('tt0121067', 'Alyas Batman en Robin', '1991', 'Action,Comedy,Crime', '5.2'), 
                                    ('tt0361763', 'James Batman', '1966', 'Action,Adventure,Comedy', '5.6'), 
                                    ('tt0372784', 'Batman Begins', '2005', 'Action,Crime,Drama', '8.2'), 
                                    ('tt10327712', 'Lego DC Batman: Family Matters', '2019', 'Action,Animation,Comedy', '6.1')]
    
def test_search_show():

    conn = sqlite3.connect("db/mydb.db")
    cursor = conn.cursor()
    search_results_list = search.search_movie("The Mandalorian", conn, cursor)
    # The Mandalorian is not valid as it is a TV Show not a Movie
    assert search_results_list == []

