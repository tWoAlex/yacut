from http import HTTPStatus

from flask import abort, flash, redirect, render_template, request

from . import app, db
from .forms import YaCutForm
from .models import URLMap


def original_link(short_id: str):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is not None:
        return link.original


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = YaCutForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data

        if not short:
            short = None
        else:
            if URLMap.query.filter_by(short=short).first() is not None:
                flash('Эта короткая ссылка уже занята!', 'already_exists')
                return render_template('index.html', form=form)

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        flash(request.host_url + short, 'success')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:short_id>/')
def redirect_from_short(short_id: str):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    original = url_map.original
    if 'http' not in original:
        original = f'http://{original}'
    return redirect(original)
