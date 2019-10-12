from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from db import get_db

bp = Blueprint('blog', __name__)
@bp.route('/')
def index():
    db =get_db()
    posts = db.execute('select p.id, title, body, created, author_id, username '
                       ' from post p join user u on p.author_id = u.id '
                       ' order by created desc'
                       ).fetchall()
    return render_template('blog/index.html', posts=posts)



