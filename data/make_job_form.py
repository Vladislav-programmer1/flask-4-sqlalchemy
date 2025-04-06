from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, IntegerRangeField
from wtforms.validators import DataRequired


class MakeJobForm(FlaskForm):
    title = StringField("Название работы", validators=[DataRequired()])
    team_leader_id = IntegerField("id Лидера команды", validators=[DataRequired()])
    work_size = IntegerField("Длительность работы", validators=[DataRequired()])
    collaborators = StringField("Исполнители", validators=[DataRequired()])
    is_finished = BooleanField("Завершена")
    submit = SubmitField("Создать")