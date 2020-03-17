from application import app, db
from flask import render_template, request, url_for, redirect
from application.reseptit.models import Resepti

@app.route("/reseptit", methods=["GET"])
def reseptit_index():
    return render_template("reseptit/list.html", reseptit = Resepti.query.all())

@app.route("/reseptit/new/")
def reseptit_form():
    return render_template("reseptit/new.html")

@app.route("/reseptit/<resepti_id>/", methods=["POST"])
def reseptit_set_cooktime(resepti_id):
    r = Resepti.query.get(resepti_id)
    r.cooktime = request.form.get("cooktime")
    db.session().commit()
    
    return redirect(url_for("reseptit_index"))

@app.route("/reseptit/", methods=["POST"])
def reseptit_create():
    r = Resepti(request.form.get("name"), request.form.get("cooktime"))
   

    db.session().add(r)
    db.session().commit()

    return redirect(url_for("reseptit_index"))
