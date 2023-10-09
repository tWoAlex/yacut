from datetime import datetime
from random import choices
from string import ascii_letters, digits

from yacut import db


SHORTLINKS_ABC = ascii_letters + digits
SHORTLINKS_DEFAULT_LENGTH = 6
SHORTLINKS_MAX_LENGTH = 16


def get_unique_short_id():
    return ''.join(choices(SHORTLINKS_ABC, k=SHORTLINKS_DEFAULT_LENGTH))


def short_is_correct(short: str) -> bool:
    if not isinstance(short, str):
        return False
    if not (0 < len(short) <= SHORTLINKS_MAX_LENGTH):
        return False
    for character in short:
        if character not in SHORTLINKS_ABC:
            return False
    return True


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True,
                      index=True, default=get_unique_short_id)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        short = data.get('custom_id', None)
        if short is not None:
            setattr(self, 'short', short)

    def to_dict(self, host: str = '') -> dict:
        return {'url': self.original,
                'short_link': host + self.short}
