import database_main


def test_connection():
    database = database_main.Database()
    database.connection.connect()
    assert database.connection.is_connected()
    database.connection.close()
    del database


def test_database_tables():
    database = database_main.Database()
    database.connection.connect()
    cursor = database.connection.cursor()
    test_query = 'SHOW TABLES'
    cursor.execute(test_query)
    test_data = set(x[0] for x in cursor.fetchall())
    assert test_data == {'students', 'rooms'}
