"""Task 05 — Tags feature tests."""
import pytest


def post_note(client, title="Test", body="Body", tags=""):
    return client.post(
        "/notes/new",
        data={"title": title, "body": body, "tags": tags},
        follow_redirects=True,
    )


def test_tags_stored_on_note(app, client):
    post_note(client, title="Note A", tags="work,personal")
    assert app.notes[0]["tags"] == ["work", "personal"]


def test_duplicate_tags_removed(app, client):
    post_note(client, title="Note B", tags="work,work,personal")
    assert app.notes[0]["tags"] == ["work", "personal"]


def test_note_without_tags_has_empty_list(app, client):
    post_note(client, title="Note C", tags="")
    assert app.notes[0]["tags"] == []


def test_tags_display_on_homepage(app, client):
    post_note(client, title="Note D", tags="science")
    response = client.get("/")
    assert b"science" in response.data


def test_filter_by_tag_shows_matching(app, client):
    post_note(client, title="Work Note", tags="work")
    post_note(client, title="Personal Note", tags="personal")
    response = client.get("/?tag=work")
    assert b"Work Note" in response.data


def test_filter_by_tag_hides_nonmatching(app, client):
    post_note(client, title="Work Note", tags="work")
    post_note(client, title="Personal Note", tags="personal")
    response = client.get("/?tag=work")
    assert b"Personal Note" not in response.data


def test_filter_all_shows_everything(app, client):
    post_note(client, title="Note X", tags="alpha")
    post_note(client, title="Note Y", tags="beta")
    response = client.get("/")
    assert b"Note X" in response.data
    assert b"Note Y" in response.data
