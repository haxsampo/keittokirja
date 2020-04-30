from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, FieldList, FormField, TextAreaField
from wtforms.widgets import TextArea


class AinesosaForm(FlaskForm):
    name = StringField("Ainesosa name", [validators.Length(min=2)])
    amount = IntegerField("Ainesosa amount")

    class Meta:
        csrf = False

class AdditionalAineetList(FlaskForm):
    aineet = FieldList(FormField(AinesosaForm), min_entries=15, max_entries=20)
    
    class Meta:
        csrf = False

