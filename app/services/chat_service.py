from app.databases.postgres import get_connection

# Pressupostos sobre get_connection():
# - retorna uma conexão do psycopg 3 (psycopg.connect(...))
# - usa row_factory=dict_row, para que fetchall()/fetchone() devolvam dicts
#   (com psycopg2, use cursor_factory=RealDictCursor e troque
#   connection.execute(...) por connection.cursor().execute(...))


def criar_chat():
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO chat DEFAULT VALUES
            RETURNING id
            """
        )

        chat_id = cursor.fetchone()["id"]
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return chat_id


def criar_mensagem(chat_id: int, content: str, role: str):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO message (content, role, chat_id)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (content, role, chat_id)
        )

        message_id = cursor.fetchone()["id"]
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return message_id


def listar_chats():
    connection = get_connection()

    try:
        chats = connection.execute(
            """
            SELECT id
            FROM chat
            ORDER BY id
            """
        ).fetchall()
    finally:
        connection.close()

    return [dict(chat) for chat in chats]


def listar_mensagens(chat_id: int):
    connection = get_connection()

    try:
        messages = connection.execute(
            """
            SELECT id, content, role, sent_at, chat_id
            FROM message
            WHERE chat_id = %s
            ORDER BY sent_at ASC, id ASC
            """,
            (chat_id,)
        ).fetchall()
    finally:
        connection.close()

    return [dict(message) for message in messages]


def deletar_chat(chat_id: int):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM chat
            WHERE id = %s
            """,
            (chat_id,)
        )

        deletado = cursor.rowcount > 0
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return deletado