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
