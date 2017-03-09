import sqlite3

def connect_to_db(db_file):
    db_connection = sqlite3.connect(db_file)
    db_connection \
        .cursor() \
        .execute('''CREATE TABLE IF NOT EXISTS notes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            text TEXT NOT NULL UNIQUE
        )''')
    db_connection.commit()

    return db_connection

def insert_in_db(db_connection, text):
    db_connection.cursor().execute('INSERT INTO notes(text) VALUES(?)', (text,))
    db_connection.commit()

def exists_in_db(db_connection, text):
    (counter,) = db_connection \
        .cursor() \
        .execute('SELECT count(*) FROM notes WHERE text = ?', (text,)) \
        .fetchone()

    return bool(counter)

def close_connection_to_db(db_connection):
    if db_connection is not None:
        db_connection.close()
