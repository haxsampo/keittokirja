from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class ReseptiForm(FlaskForm):
    name = StringField("Resepti name", [validators.Length(min=2)])
    cooktime = IntegerField("Resepti cooktime")

    class Meta:
        csrf = False

class SearchForm(FlaskForm):
    search = StringField("Search ainesosa")
    
    class Meta:
        csrf = False