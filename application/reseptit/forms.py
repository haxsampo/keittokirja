from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class TaskForm(FlaskForm):
    name = StringField("Resepti name", [validators.Length(min=2)])
    cooktime = IntegerField("Resepti cooktime")

    class Meta:
        csrf = False