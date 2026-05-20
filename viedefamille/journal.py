from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from viedefamille.auth import login_required
from viedefamille.db import get_db

bp = Blueprint("journal", __name__)
