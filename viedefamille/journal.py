from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from viedefamille.auth import login_required
from viedefamille.db import get_db

bp = Blueprint("journal", __name__)


@bp.route("/")
def index():
    db = get_db()
    log_entries = db.execute(
        "SELECT *"
        " FROM log_entry e JOIN user u ON e.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("journal/index.html", log_entries=log_entries)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        author_id = g.user["id"]
        entry_type = request.form["entry_type"]
        family_member_id = request.form["family_member_id"]
        amount = request.form["amount"]
        comments = request.form["comments"]
        error = None

        if not entry_type:
            error = "Entry type is required."

        if error is not None:
            flash(error)
        else:
            created = get_db().execute("SELECT CURRENT_TIMESTAMP").fetchone()[0]

            db = get_db()
            db.execute(
                "INSERT INTO log_entry "
                "(author_id, entry_type, created, "
                "family_member_id, amount, comments)"
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    author_id,
                    entry_type,
                    created,
                    family_member_id,
                    amount,
                    comments,
                ),
            )
            db.commit()
            return redirect(url_for("journal.index"))

    return render_template("journal/create.html")


def get_log_entry(id, check_author=True):
    log_entry = (
        get_db()
        .execute(
            "SELECT e.id, u.username, e.entry_type, e.family_member_id, e.amount, e.comments, e.author_id"
            " FROM log_entry e JOIN user u ON e.author_id = u.id"
            " WHERE e.id = ?",
            (id,),
        )
        .fetchone()
    )

    if log_entry is None:
        abort(404, f"Log entry id {id} doesn't exist.")

    if check_author and log_entry["author_id"] != g.user["id"]:
        abort(403)

    return log_entry


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    log_entry = get_log_entry(id)

    if request.method == "POST":
        entry_type = request.form["entry_type"]
        family_member_id = request.form["family_member_id"]
        amount = request.form["amount"]
        comments = request.form["comments"]
        error = None

        if not entry_type:
            error = "Entry type is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE log_entry SET entry_type = ?, family_member_id = ?, amount = ?, comments = ?"
                " WHERE id = ?",
                (
                    entry_type,
                    family_member_id,
                    amount,
                    comments,
                    id,
                ),
            )
            db.commit()
            return redirect(url_for("journal.index"))

    return render_template("journal/update.html", log_entry=log_entry)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    get_log_entry(id)
    db = get_db()
    db.execute("DELETE FROM log_entry WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("journal.index"))
