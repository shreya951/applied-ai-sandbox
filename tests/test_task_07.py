"""Task 07 — Starred notes tests."""


def post_note(client, title="Test", body="Body", tags=""):
    return client.post(
        "/notes/new",
        data={"title": title, "body": body, "tags": tags},
        follow_redirects=True,
    )


def star(client, idx):
    return client.post(f"/notes/{idx}/star", follow_redirects=True)


def test_new_note_is_not_starred(app, client):
    post_note(client, title="Note A")
    assert app.notes[0]["is_starred"] is False


def test_star_note_toggles_true(app, client):
    post_note(client, title="Note A")
    star(client, 0)
    assert app.notes[0]["is_starred"] is True


def test_star_note_toggles_back(app, client):
    post_note(client, title="Note A")
    star(client, 0)
    star(client, 0)
    assert app.notes[0]["is_starred"] is False


def test_star_nonexistent_returns_404(app, client):
    response = client.post("/notes/99/star")
    assert response.status_code == 404


def test_starred_note_appears_first(app, client):
    post_note(client, title="Note A")
    post_note(client, title="Note B")
    star(client, 1)  # star Note B (index 1)
    response = client.get("/")
    html = response.data.decode()
    assert html.index("Note B") < html.index("Note A")


def test_star_icon_in_homepage_html(app, client):
    post_note(client, title="Note A")
    response = client.get("/")
    assert "☆" in response.data.decode() or "★" in response.data.decode()
