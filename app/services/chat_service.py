from app.databases.lite import get_connection

def criar_chat():
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO chat DEFAULT VALUES
        """
    )

    connection.commit()
    chat_id = cursor.lastrowid
    connection.close()

    return chat_id


def criar_mensagem(chat_id: int, content: str, role: str):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO message (content, role, chat_id)
        VALUES (?, ?, ?)
        """,
        (content, role, chat_id)
    )

    connection.commit()
    message_id = cursor.lastrowid
    connection.close()

    return message_id


def listar_chats():
    connection = get_connection()

    chats = connection.execute(
        """
        SELECT id
        FROM chat
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    return [dict(chat) for chat in chats]


def listar_mensagens(chat_id: int):
    connection = get_connection()

    messages = connection.execute(
        """
        SELECT id, content, role, sent_at, chat_id
        FROM message
        WHERE chat_id = ?
        ORDER BY sent_at ASC, id ASC
        """,
        (chat_id,)
    ).fetchall()

    connection.close()

    return [dict(message) for message in messages]


def deletar_chat(chat_id: int):
    connection = get_connection()

    cursor = connection.execute(
        """
        DELETE FROM chat
        WHERE id = ?
        """,
        (chat_id,)
    )

    connection.commit()
    deletado = cursor.rowcount > 0
    connection.close()

    return deletado