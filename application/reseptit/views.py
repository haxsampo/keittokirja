from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user

from application import app, db
from application.reseptit.forms import ReseptiForm
from application.reseptit.forms import SearchForm
from application.reseptit.forms import NewReseptiForm
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
    return render_template("reseptit/new.html", form = NewReseptiForm())

@app.route("/reseptit/edit/<resepti_id>/")
@login_required
def resepti_edit(resepti_id):
    form = NewReseptiForm()
    r = Resepti.query.get(resepti_id)
    form.resepti.name.data = r.name
    form.resepti.cooktime.data = r.cooktime
    o = Ohje.query.filter_by(resepti_id=resepti_id).first()
    form.ohje.data = o.ohjeet
    a = Ainesosa.find_ainesosat_for_recipe(resepti_id)
    ##Lisää ainesosapaskat tänne
    return render_template("reseptit/edit.html", form = form)


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
    poistettava = Resepti.query.get(resepti_id)
    db.session.delete(poistettava)
    db.session.commit()
    Ainesosa.clean_ainesosat()
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
    a = Ainesosa.find_ainesosat_for_recipe(resepti_id)
    o = Ohje.find_ohje_with_id(resepti_id)
    return render_template("reseptit/show.html", resepti= r, ainesosat = a, ohje = o)


@app.route("/reseptit/", methods=["POST"])
@login_required
def reseptit_create():
    form = NewReseptiForm(request.form)
   
    #print(form.resepti.ohje.data)
    if not form.resepti.validate(form):
        return render_template("reseptit/new.html", form = form)
    if not form.aineet.validate(form):
        return render_template("reseptit/new.html", form = form)

    #Add only those aine forms with info to list
    aineListWithoutEmpties = []
    name = ""
    for key in form.aineet.data:
        if "name" in key:
            name = form.aineet.data[key]
        if "amount" in key and name:
            #lisää tänne if amount = none niin laittaa sinne vaikka nollan?
            aineListWithoutEmpties.append({name: form.aineet.data[key]})

    r = Resepti(form.resepti.nimi.data, form.resepti.cooktime.data)
    r.account_id = current_user.id

    db.session.add(r)
    db.session().commit()
    
    
    #create and append non existing aineet, put info of existing ones in list
    alreadyInDb = []
    for aineEl in aineListWithoutEmpties:
        name = list(aineEl.keys())[0]
        aines = Ainesosa.query.filter_by(name=name).first()
        if not aines: #name of current aineEl doesn't exist in db
            a = Ainesosa(name)
            r_a = Resepti_ainesosa(amount=aineEl[name])
            r_a.ainesosa = a
            r.ainesosa.append(r_a)
        else: #name of ainesEl already exists in db -> save the queried object for id and amount from ainesform
            alreadyInDb.append({'ainesKey':aines, 'amount':aineEl[name]})


    #db.session().add(r)
    newOhje = Ohje(form.resepti.ohje.data)
    newOhje.resepti_id = r.id
    db.session().add(newOhje)
    db.session().commit()

    #Add references to resepti_ainesosa table for prexisting ones
    for ainesEl in alreadyInDb:
        Resepti_ainesosa.add_ref_to_resepti_ainesosa(r.id, ainesEl['ainesKey'].id, ainesEl['amount'])

    return redirect(url_for("reseptit_index"))
