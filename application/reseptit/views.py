from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user

from application import app, db
from application.reseptit.forms import ReseptiForm, SearchForm, NewReseptiForm, EditForm
from application.reseptit.models import Resepti
from application.misc.sqlhelp import requestContainer
from application.ohje.models import Ohje
from application.ainesosat.models import Ainesosa
from application.resepti_ainesosat.models import Resepti_ainesosa

@app.route("/reseptit", methods=["GET"])
def reseptit_index():
    ainesosaCount = Resepti.find_resepti_ainesosa_count()
    return render_template("reseptit/list.html", reseptit = Resepti.query.all(), ainesosaCount = ainesosaCount)

@app.route("/reseptit/new/")
@login_required
def reseptit_form():
    return render_template("reseptit/new.html", form = NewReseptiForm())

@app.route("/reseptit/edit/<resepti_id>/")
@login_required
def resepti_edit(resepti_id):
    form = EditForm()
    r = Resepti.query.get(resepti_id)
    form.resepti.nimi.data = r.name
    form.resepti.cooktime.data = r.cooktime
    o = Ohje.query.filter_by(resepti_id=resepti_id).first()
    form.resepti.ohje.data = o.ohjeet

    a = Ainesosa.find_ainesosat_for_recipe(resepti_id)
    print(a)
    try:
        form.aineet.name0.data = a[0]['name']
        form.aineet.amount0.data = a[0]['amount']
    except Exception as e:
        print(e)
        pass 
    try:
        form.aineet.name1.data = a[1]['name']
        form.aineet.amount1.data = a[1]['amount']
    except:
        print("virhe tokassa")
        pass
    try:
        form.aineet.name2.data = a[2]['name']
        form.aineet.amount2.data = a[2]['amount']
    except:
        pass
    return render_template("reseptit/edit.html", form = form, resepti_id = resepti_id)


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
    if current_user.user_group != 0:
        flash("Deleting is for admin users")
        return render_template("index.html")
    poistettava = Resepti.query.get(resepti_id)
    db.session.delete(poistettava)
    db.session.commit()
    Ainesosa.clean_ainesosat()
    ainesosaCount = Resepti.find_resepti_ainesosa_count()
    return render_template("reseptit/list.html", reseptit=Resepti.query.all(), ainesosaCount = ainesosaCount)

@app.route("/reseptit/<resepti_id>/", methods=["POST", "GET", "DELETE"])
@login_required
def reseptit_set_cooktime(resepti_id):
    if  request.method == 'POST':
        ##Edit resepti with resepti_id
        form = EditForm(request.form)

        if not form.resepti.validate(form):
            return render_template("reseptit/edit.html", form = form)
        if not form.aineet.validate(form):
            return render_template("reseptit/edit.html", form = form)

        r = Resepti.query.get(resepti_id)   

        newCooktime = form.resepti.cooktime.data
        if newCooktime:
            r.cooktime = newCooktime
            
        newName = form.resepti.nimi.data
        if newName:
            r.name = newName

        o = Ohje.query.filter_by(resepti_id = resepti_id).first()
        newOhje = form.resepti.ohje.data
        if newOhje:
            o.ohjeet = newOhje

        #Luodaan lista ainesosaformeien sisällöistä
        aineList = []
        if form.aineet.name0.data:
            aineList.append({'aine':form.aineet.name0.data, 'amount' : form.aineet.amount0.data})
        if form.aineet.name1.data:
            aineList.append({'aine': form.aineet.name1.data, 'amount': form.aineet.amount1.data})
        if form.aineet.name2.data:
            aineList.append({'aine': form.aineet.name2.data, 'amount': form.aineet.amount2.data})

        #Tehdään lista käsiteltäville resepti_ainesosa.id:lle myöhempää tietokannan siivoamista varten
        relevantAinesosaId = []
        #Lista uusille ainesosille, jos niitä ei ole vielä olemassa
        #Nämä saavat id:t vasta commitin jälkeen, joten näille voidaan luoda resepti_ainesosa-linkit vasta tämän jälkeen
        newAinesosaList = []
        for aine in aineList:
            aineExists = Ainesosa.query.filter_by(name=aine['aine']).first()
            if aineExists:#ainesosa on olemassa
                relevantAinesosaId.append(aineExists.id)
                res_aine = Resepti_ainesosa.query.filter_by(resepti_id=resepti_id, ainesosa_id=aineExists.id).first()
                if res_aine: #resepti_ainesosa on olemassa, update amount
                    print("res_aine: ", res_aine)
                    print("res_aine amount: ", aine['amount'])
                    res_aine.amount = aine['amount']
                else: #resepti_ainesosa ei ole olemassa, create
                    Resepti_ainesosa.add_ref_to_resepti_ainesosa(resepti_id, aineExists.id, aine['amount'])
            else: #ainesosa ei ole olemassa, lisätään sessioon ja listalle, niin voidaan myöhemmin tehdä resepti_ainesosat id:iden muodostuttua committissa
                newAinesosa = Ainesosa(aine['aine'])
                newAinesosaList.append({'newAines':newAinesosa, 'amount':aine['amount']})
                db.session().add(newAinesosa)
        print("newAinesosaList: ",newAinesosaList)
        print("relevantAinesosaId: ", relevantAinesosaId)
        db.session().commit()

        #luodaan resepti_ainesosat juuri luoduille ainesosille
        for el in newAinesosaList:
            relevantAinesosaId.append(el['newAines'].id)
            Resepti_ainesosa.add_ref_to_resepti_ainesosa(resepti_id, el['newAines'].id, el['amount'])

        #siistitään tietokannasta sellaiset rivit jotka ovat jääneet ilman linkkejä tämän funktion käpistelyn seurauksena
        Resepti_ainesosa.delete_non_relevant_resepti_ainesosa(resepti_id, relevantAinesosaId)
        Ainesosa.clean_ainesosat()
        
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
