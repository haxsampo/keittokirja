from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, FieldList, FormField

class ReseptiForm(FlaskForm):
    name = StringField("Resepti name", [validators.Length(min=2)])
    cooktime = IntegerField("Resepti cooktime")
    #ainesosa = StringField("Resepti ainesosa", [validators.Length(min=2)])

    class Meta:
        csrf = False

class SearchForm(FlaskForm):
    search = StringField("Search ainesosa")
    
    class Meta:
        csrf = False

class AinesosaForm(FlaskForm):
    name = StringField("Ainesosa name", [validators.Length(min=2)])
    amount = IntegerField("Ainesosa amount")

    class Meta:
        csrf = False

class AineetList(FlaskForm):
    aineet = FieldList(FormField(AinesosaForm), min_entries=2, max_entries=20)
    
    class Meta:
        csrf = False

