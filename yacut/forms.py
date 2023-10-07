from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional


class YaCutForm(FlaskForm):
    original_link = URLField(label='Введите ссылку, которую хотите сократить',
                             validators=(DataRequired(),))
    custom_id = StringField(label='Желаемый короткий ID',
                            validators=(Optional(),))
    submit = SubmitField(label='Создать')
