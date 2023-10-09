from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional


class YaCutForm(FlaskForm):
    original_link = URLField(
        label='Длинная ссылка',
        validators=(DataRequired('Длинная ссылка не может быть пустой'),)
    )
    custom_id = StringField(label='Ваш вариант короткой ссылки',
                            validators=(Optional(),))
    submit = SubmitField(label='Создать')
