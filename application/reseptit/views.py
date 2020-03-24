from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user

from application import app, db
from application.reseptit.forms import TaskForm
from application.reseptit.models import Resepti

@app.route("/reseptit", methods=["GET"])
def reseptit_index():
    return render_template("reseptit/list.html", reseptit = Resepti.query.all())

@app.route("/reseptit/new/")
@login_required
def reseptit_form():
    return render_template("reseptit/new.html", form = TaskForm())

@app.route("/reseptit/<resepti_id>/", methods=["POST"])
@login_required
def reseptit_set_cooktime(resepti_id):
    form = TaskForm(request.form)

    if not form.validate():
        print("not validated")
        return redirect(url_for("reseptit_index"))

    r = Resepti.query.get(resepti_id)   

    newCooktime = request.form.get("cooktime")
    if newCooktime:
        r.cooktime = newCooktime
        
    newName = request.form.get("name")
    if newName:
        r.name = newName
    
    db.session().commit()
    print("session committed")
    
    return redirect(url_for("reseptit_index"))

@app.route("/reseptit/", methods=["POST"])
@login_required
def reseptit_create():
    form = TaskForm(request.form)

    if not form.validate():
        return render_template("reseptit/new.html", form = form)

    r = Resepti(form.name.data, form.cooktime.data)
    r.account_id = current_user.id


    db.session().add(r)
    db.session().commit()

    return redirect(url_for("reseptit_index"))
