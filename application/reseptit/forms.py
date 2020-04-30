from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, FieldList, FormField, TextAreaField
from wtforms.widgets import TextArea

class AinesosaForm(FlaskForm):
    name = StringField("Ainesosa name")
    amount = IntegerField("Ainesosa amount")
    name1 = StringField("Ainesosa name")
    amount1 = IntegerField("Ainesosa amount", validators=(validators.Optional(),))
    name2 = StringField("Ainesosa name")
    amount2 = IntegerField("Ainesosa amount", validators=(validators.Optional(),))

    class Meta:
        csrf = False

class EditAinesosaForm(FlaskForm):
    name0 = StringField("Ainesosa name", [validators.Length(max=40)])
    amount0 = IntegerField("Ainesosa amount")
    name1 = StringField("Ainesosa name")
    amount1 = IntegerField("Ainesosa amount", validators=(validators.Optional(),))
    name2 = StringField("Ainesosa name")
    amount2 = IntegerField("Ainesosa amount", validators=(validators.Optional(),))

    class Meta:
        csrf = False

class ReseptiForm(FlaskForm):
    nimi = StringField("Resepti name", [validators.Length(min=2, max=30)])
    cooktime = IntegerField("Resepti cooktime", [validators.NumberRange(min=1, max=2800)])
    ohje = TextAreaField("Reseptin ohjeet", [validators.Length(min=2, max=500)])

    class Meta:
        csrf = False

class NewReseptiForm(FlaskForm):
    resepti = FormField(ReseptiForm)
    aineet = FormField(AinesosaForm)
    

    class Meta:
        csrf = False

class SearchForm(FlaskForm):
    search = StringField("Search ainesosa")
    
    class Meta:
        csrf = False

class EditForm(FlaskForm):
    resepti = FormField(ReseptiForm)
    aineet = FormField(EditAinesosaForm)

    class Meta:
        csrf = False

class EditAinesosaForm(FlaskForm):
    name0 = StringField("Ainesosa name")
    amount0 = IntegerField("Ainesosa amount")
    name1 = StringField("Ainesosa name")
    amount1 = IntegerField("Ainesosa amount", validators=(validators.Optional(),))
    name2 = StringField("Ainesosa name")
    amount2 = IntegerField("Ainesosa amount", validators=(validators.Optional(),))

    class Meta:
        csrf = False
