from application import app, db
from flask import render_template, request
from application.reseptit.models import Resepti

@app.route("/reseptit/new/")
def reseptit_form():
    return render_template("reseptit/new.html")

@app.route("/reseptit/", methods=["POST"])
def reseptit_create():
    r = Resepti(request.form.get("name"))

    db.session().add(r)
    db.session().commit()

    return "tämä tulee reseptit/views.py:stä"