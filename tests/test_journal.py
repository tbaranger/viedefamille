import pytest
from viedefamille.db import get_db


def test_index(client, auth):
    response = client.get("/")
    data = response.get_data(as_text=True)
    assert "Se connecter" in data
    assert "Créer un compte" in data

    auth.login()
    response = client.get("/")
    data = response.get_data(as_text=True)
    assert "Se déconnecter" in data


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    # change the entry author to another user
    with app.app_context():
        db = get_db()
        db.execute("UPDATE log_entry SET author_id = 2 WHERE id = 1")
        db.commit()

    auth.login()
    # current user can't modify other user's entry
    assert client.post("/1/update").status_code == 403
    assert client.post("/1/delete").status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get("/").data


@pytest.mark.parametrize(
    "path",
    (
        "/2/update",
        "/2/delete",
    ),
)
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get("/create").status_code == 200
    client.post("/create", data={"title": "created", "body": ""})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM log_entry").fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/1/update").status_code == 200
    client.post("/1/update", data={"title": "updated", "body": ""})

    with app.app_context():
        db = get_db()
        entry = db.execute("SELECT * FROM log_entry WHERE id = 1").fetchone()
        assert entry["title"] == "updated"


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
    ),
)
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"entry_type": "", "body": ""})
    assert b"Title is required." in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/delete")
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        entry = db.execute("SELECT * FROM log_entry WHERE id = 1").fetchone()
        assert entry is None
