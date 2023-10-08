from http import HTTPStatus

from flask import jsonify, render_template

from . import app


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str, status_code: int = None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error) -> (str, int):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
