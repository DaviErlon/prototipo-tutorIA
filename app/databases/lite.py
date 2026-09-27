import sqlite3

DATABASE = "chat.db"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    
    # caso seja operação de deletar chat
    connection.execute("PRAGMA foreign_keys = ON") 

    return connection

def create_tables():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
            sent_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            chat_id INTEGER NOT NULL,

            FOREIGN KEY (chat_id)
                REFERENCES chat(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()

create_tables()