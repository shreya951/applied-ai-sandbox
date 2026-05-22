"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for, abort


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        tag_filter = request.args.get("tag", "")
        indexed = [
            (i, n) for i, n in enumerate(app.notes)
            if not tag_filter or tag_filter in n.get("tags", [])
        ]
        indexed_sorted = sorted(indexed, key=lambda x: not x[1].get("is_starred", False))
        all_tags = sorted({t for n in app.notes for t in n.get("tags", [])})
        return render_template(
            "home.html",
            notes=indexed_sorted,
            all_tags=all_tags,
            current_tag=tag_filter,
        )

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            raw_tags = request.form.get("tags") or ""
            tags = list(dict.fromkeys(
                t for t in (t.strip() for t in raw_tags.split(",")) if t
            ))
            error_title = "Title is required" if not title else None
            error_body = "Body is required" if not body else None
            if error_title or error_body:
                return render_template(
                    "new_note.html",
                    title=title,
                    body=body,
                    tags_value=raw_tags,
                    error_title=error_title,
                    error_body=error_body,
                )
            app.notes.append({"title": title, "body": body, "tags": tags, "is_starred": False})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    @app.route("/notes/<int:idx>/star", methods=["POST"])
    def star_note(idx):
        if idx < 0 or idx >= len(app.notes):
            abort(404)
        app.notes[idx]["is_starred"] = not app.notes[idx].get("is_starred", False)
        return redirect(url_for("home"))

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
