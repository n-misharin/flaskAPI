from flask import Blueprint, request, session

from app.database import auth, register_user, get_articles, get_article_by_id, insert_article, get_user_by_login

module = Blueprint("main", __name__, url_prefix="/")


@module.get("/")
def index():
    if "username" in session:
        return {
            "status": "OK",
            "message": f"Привет, {session['username']}."
        }
    return {
        "status": "OK",
        "message": f"Войдите в систему."
    }


@module.post("/registration")
def registration():
    data = request.get_json()
    try:
        register_user(data["login"], data["password"])
        session["username"] = data["login"]
        return {
            "status": "accepted",
            "message": "OK",
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": str(e)
        }


@module.post("/authentication")
def login():
    data = request.get_json()
    if auth(data["login"], data["password"]) is None:
        return {
            "status": "failed",
            "message": "Неверный логин или пароль"
        }
    session["username"] = data["login"]
    return {
        "status": "accepted",
        "message": "OK",
    }


@module.get("/logout")
def logout():
    session.clear()
    return {
        "status": "accepted",
        "message": "OK"
    }


@module.get("/articles")
def articles():
    return {
        "articles": get_articles()
    }


@module.get("/article/<int:id>")
def article(id):
    return {
        "article": get_article_by_id(id)
    }


@module.post("/article")
def article_create():
    if "username" not in session:
        return {
            "status": "failed",
            "message": "Для добавления статьи нужно авторизоваться!"
        }
    data = request.get_json()
    user = get_user_by_login(session["username"])
    article_id = insert_article(data["title"], data["body"], user["id"])
    return {
        "article": get_article_by_id(article_id)
    }
