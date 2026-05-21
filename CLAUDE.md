# CLAUDE.md

Context Claude Code reads automatically when started in this repo.

## What this project is

A tiny Flask web application used as the practice playground for the
**Code2College Applied AI Cohort**. It's intentionally incomplete — each
task in `tasks/` walks the student through fixing or adding one piece.

## Stack

- Python 3.10+
- Flask 3.x
- pytest
- Jinja2 templates, vanilla HTML/CSS

## How to run things

```bash
# Run the app
python app.py
# → http://localhost:5000

# Run all tests
pytest

# Run tests for a single task
pytest tests/test_task_01.py
```

## Conventions

- Each task corresponds to a `tests/test_task_NN.py` file. The task is
  "done" when those tests pass.
- Don't edit `tests/` to make them pass — change `app.py` / `templates/`
  instead.
- Keep changes scoped to the task. Don't refactor unrelated files.
- When unsure, prefer reading the test file first — it tells you exactly
  what behavior is expected.

## Auth conventions

- Authentication is handled via Flask sessions (`flask.session`).
- Never store plaintext passwords — hash with `werkzeug.security` (`generate_password_hash` / `check_password_hash`).
- Protect routes that require login with a `@login_required` decorator (or an explicit `session` check at the top of the view).
- On logout, call `session.clear()` rather than deleting individual keys.
- Don't roll custom crypto; use the helpers already in the stack.

## Working with Claude here

- Always read the task file before writing code.
- Plan before implementing — ask Claude for a plan first.
- Run `pytest` after each substantive change.
- If Claude proposes editing a test to "make it pass," push back. The
  tests are the spec.
