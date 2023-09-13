from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired


class LessonForm(FlaskForm):
    First = StringField('Название фильма', validators=[DataRequired()])
    description = TextAreaField('Описание фильма')
    year = IntegerField('Год создания')
    genre = StringField('Жанр фильма')
    rating = FloatField('Оценка на Кинопоиске')
    age_limit = StringField('Возраст')
    foto = StringField('Изображение')
    submit = SubmitField('Добавить')