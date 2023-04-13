import sqlite3

db = sqlite3.connect("database.db", check_same_thread=False)


def get_user_by_login(login: str) -> dict | None:
    res = db.execute(
        """SELECT * FROM users WHERE login = ?""",
        (login, )
    )
    user = res.fetchone()
    if user is None:
        return None
    return {
        "id": user[0],
        "login": user[1],
        "password": user[2],
    }


def auth(login: str, password: str) -> str | None:
    res = db.execute(
        """SELECT * FROM users WHERE login = ? AND password = ?""",
        (login, password,)
    )
    if res.fetchone() is None:
        return None
    return login


def register_user(login: str, password: str) -> None:
    try:
        db.execute(
            """INSERT INTO users (login, password) VALUES (?, ?)""",
            (login, password)
        )
        db.commit()
    except Exception:
        raise Exception("Такой пользователь уже существует!")


def get_articles() -> list[dict]:
    res = db.execute(
        """
        SELECT *  
        FROM articles 
        JOIN users
        ON users.id = articles.author_id
        """
    )
    articles = []
    for article in res.fetchall():
        # print(article)
        articles.append({
            "id": article[0],
            "title": article[1],
            "body": article[2],
            "author": {
                "id": article[3],
                "login": article[5]
            }
        })
    return articles


def get_article_by_id(_id: int) -> dict:
    print("воть", _id)
    res = db.execute(
        """
        SELECT * 
        FROM articles
        JOIN users
        ON users.id = articles.author_id
        WHERE articles.id = ?
        """,
        (_id, )
    )
    article = res.fetchone()
    print(article)
    if article is None:
        return {}
    return {
        "id": article[0],
        "title": article[1],
        "body": article[2],
        "author": {
            "id": article[3],
            "login": article[5],
        }
    }


def insert_article(title: str, body: str, author_id) -> int | None:
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO articles (title, body, author_id)
            VALUES (?, ?, ?)
            """,
            (title, body, author_id)
        )
        db.commit()
        return cursor.lastrowid
    except Exception:
        return None

