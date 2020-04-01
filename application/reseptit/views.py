from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user

from application import app, db
from application.reseptit.forms import ReseptiForm
from application.reseptit.forms import SearchForm
from application.reseptit.models import Resepti
from application.misc.sqlhelp import requestContainer
from application.reseptit.models import Ainesosa

@app.route("/reseptit", methods=["GET"])
def reseptit_index():
    return render_template("reseptit/list.html", reseptit = Resepti.query.all())

@app.route("/reseptit/new/")
@login_required
def reseptit_form():
    return render_template("reseptit/new.html", form = ReseptiForm())

@app.route("/search/")
@login_required
def reseptit_search():
    return render_template("reseptit/search.html", form = SearchForm())

@app.route("/search/", methods=["POST"])
@login_required
def reseptit_search_with_stuff():
    form = SearchForm()
    reseptit = Resepti.find_reseptit_with_arg_ainesosa(request.form.get("search"))
    return render_template("reseptit/search.html", form = form, reseptit = reseptit)



@app.route("/reseptit/<resepti_id>/", methods=["POST", "GET"])
@login_required
def reseptit_set_cooktime(resepti_id):
    ##Edit resepti with resepti_id
    if request.method == "POST":
        form = ReseptiForm(request.form)

        r = Resepti.query.get(resepti_id)   

        newCooktime = request.form.get("cooktime")
        if newCooktime:
            r.cooktime = newCooktime
        else:
            del form.cooktime
            
        newName = request.form.get("name")
        if newName:
            r.name = newName
        else:
            del form.name

        if not form.validate():
            print(form.errors)
            return redirect(url_for("reseptit_index"))
        
        db.session().commit()
        
        return redirect(url_for("reseptit_index"))
    ##Show resepti with resepti_id
    else:
        return redirect(url_for("reseptit_index"))

@app.route("/reseptit/", methods=["POST"])
@login_required
def reseptit_create():
    form = ReseptiForm(request.form)

    if not form.validate():
        return render_template("reseptit/new.html", form = form)

    r = Resepti(form.name.data, form.cooktime.data)
    r.account_id = current_user.id
    a = Ainesosa(form.ainesosa.data)

    #tsekataan onko ainesosa jo ainesosa-taulussa
    ainesosa = Ainesosa.query.filter_by(name=a.name).first()

    if not ainesosa:
        db.session().add(a)
        r.ainesosa.append(a) 

    db.session().add(r)
    db.session().commit()

    if ainesosa: #on taulussa
        print("#ontaulussa")
        Ainesosa.add_ref_to_resepti_ainesosa(r.id, ainesosa.id)

    return redirect(url_for("reseptit_index"))
