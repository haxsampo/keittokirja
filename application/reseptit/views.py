from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user

from application import app, db
from application.reseptit.forms import ReseptiForm
from application.reseptit.forms import SearchForm
from application.reseptit.forms import AineetList
from application.reseptit.models import Resepti
from application.misc.sqlhelp import requestContainer
from application.reseptit.models import Ainesosa
from application.reseptit.models import Resepti_ainesosa
from application.ohje.models import Ohje

@app.route("/reseptit", methods=["GET"])
def reseptit_index():
    return render_template("reseptit/list.html", reseptit = Resepti.query.all())

@app.route("/reseptit/new/")
@login_required
def reseptit_form():
    return render_template("reseptit/new.html", form = ReseptiForm(), aineet = AineetList())

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

@app.route("/reseptit/del/<resepti_id>/")
@login_required
def delete_resepti(resepti_id):
    print("TERVE DELEE_RESEPTI")
    poistettava = Resepti.query.get(resepti_id)
    db.session.delete(poistettava)
    db.session.commit()
    print("COMMITKIN TOIMII JIPPIII")
    return render_template("reseptit/list.html", reseptit=Resepti.query.all())

@app.route("/reseptit/<resepti_id>/", methods=["POST", "GET", "DELETE"])
@login_required
def reseptit_set_cooktime(resepti_id):
    if  request.method == 'POST':
        ##Edit resepti with resepti_id
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

    if  request.method == 'GET':
        r = Resepti.query.get(resepti_id)
        a = Ainesosa.find_ainesosat_for_recipe(resepti_id)
        o = Ohje.find_ohje_with_id(resepti_id)
        return render_template("reseptit/show.html", resepti= r, ainesosat = a, ohje = o)


@app.route("/reseptit/show/<resepti_id>/")
@login_required
def show_recipe(resepti_id):
    r = Resepti.query.get(resepti_id)
    print("-------------------------------------------BEGIN TRANSMISSION-------------------------------------------")
    a = Ainesosa.find_ainesosat_for_recipe(resepti_id)
    o = Ohje.find_ohje_with_id(resepti_id)
    return render_template("reseptit/show.html", resepti= r, ainesosat = a, ohje = o)


@app.route("/reseptit/", methods=["POST"])
@login_required
def reseptit_create():
    form = ReseptiForm(request.form)
    aineForm = AineetList()
    

    if not form.validate():
        return render_template("reseptit/new.html", form = form, aineet = aineForm)

    #Add only those forms with info to list
    aineListWithoutEmpties = []
    for aineEl in aineForm.aineet.data:
        elName = aineEl['name']
        if not elName == "":
            aineListWithoutEmpties.append({'name':aineEl['name'], 'amount':aineEl['amount'] })
        

    r = Resepti(form.name.data, form.cooktime.data)
    r.account_id = current_user.id

    db.session.add(r)
    db.session().commit()
    
    

    alreadyInDb = []
    for aineEl in aineListWithoutEmpties:
        aines = Ainesosa.query.filter_by(name=aineEl['name']).first()
        if not aines: #name of current aineEl doesn't exist in db
            a = Ainesosa(aineEl['name'])
            r_a = Resepti_ainesosa(amount=aineEl['amount'])
            r_a.ainesosa = a
            r.ainesosa.append(r_a)
        else: #name of ainesEl already exists in db -> save the queried object for id and amount from ainesform
            alreadyInDb.append({'ainesKey':aines, 'amount':aineEl['amount']})


    #db.session().add(r)
    newOhje = Ohje(form.ohje.data)
    newOhje.resepti_id = r.id
    db.session().add(newOhje)
    db.session().commit()

    #Add references to resepti_ainesosa table for prexisting ones
    for ainesEl in alreadyInDb:
       Resepti_ainesosa.add_ref_to_resepti_ainesosa(r.id, ainesEl['ainesKey'].id, aineEl['amount'])

    return redirect(url_for("reseptit_index"))
