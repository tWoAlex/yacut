from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap, short_is_correct
from .views import original_link


@app.route('/api/id/', methods=('POST',))
def create_short_link():
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not data['url']:
        raise InvalidAPIUsage('url не может быть пустым!')

    short = data.get('custom_id', None)
    if not short:
        short = None
    else:
        if not short_is_correct(short):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=short).first() is not None:
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict(host=request.host_url)), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original_link(short_id):
    link = original_link(short_id)
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден',
                              HTTPStatus.NOT_FOUND)
    return jsonify({'url': link}), HTTPStatus.OK
