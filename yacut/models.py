from datetime import datetime
from random import choices
from string import ascii_letters, digits

from yacut import db


SHORTLINKS_ABC = ascii_letters + digits
SHORTLINKS_LENGTH = 6


def get_unique_short_id():
    return ''.join(choices(SHORTLINKS_ABC, k=SHORTLINKS_LENGTH))


def short_is_correct(short: str) -> bool:
    for character in short:
        if character not in SHORTLINKS_ABC:
            return False
    return True


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256))
    short = db.Column(db.String(128), index=True, default=get_unique_short_id)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
        setattr(self, 'url', data['url'])
        short = data.get('custom_id', None)
        if short is not None:
            setattr(self, 'short', short)

    def to_dict(self, host: str = '') -> dict:
        return {'url': self.original,
                'short_link': host + self.short}
