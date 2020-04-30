from application import db
from application.models import Base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from sqlalchemy.sql import text

#Ainesosa-Resepti assosiaatiotaulu
#resepti_ainesosa = db.Table('resepti_ainesosa',
#                    db.Column('resepti_id', db.Integer, db.ForeignKey('resepti.id')),
#                    db.Column('ainesosa_id', db.Integer, db.ForeignKey('ainesosa.id')),
#                    db.Column('amount', db.String(32))
#                    )

class Resepti_ainesosa(db.Model):
    resepti_id = db.Column(db.Integer, db.ForeignKey('resepti.id'), primary_key=True)
    ainesosa_id = db.Column(db.Integer, db.ForeignKey('ainesosa.id'), primary_key=True)
    amount = db.Column(db.String(32))
    ainesosa = db.relationship("Ainesosa", back_populates="resepti")
    resepti = db.relationship("Resepti", back_populates="ainesosa")


    @staticmethod
    def add_ref_to_resepti_ainesosa(resepti_id, ainesosa_id, amount):
        resid = str(resepti_id)
        ainid = str(ainesosa_id)
        amountStr = str(amount)

        stmt = text("INSERT INTO resepti_ainesosa (resepti_id, ainesosa_id, amount) "
                    "VALUES (:resid, :ainid, :amountStr);").params(resid=resid, ainid=ainid, amountStr=amountStr)

        db.engine.execute(stmt)

    def delete_non_relevant_resepti_ainesosa(resepti_id, ainesosa_ids):
        resid = str(resepti_id)
        if len(ainesosa_ids) == 0:
            stmt = text("DELETE FROM resepti_ainesosa WHERE resepti_id = :resid;").params(resid=resid)
            db.engine.execute(stmt)
        elif len(ainesosa_ids) == 1:
            ainid = str(ainesosa_ids[0])
            stmt = text("DELETE FROM resepti_ainesosa WHERE resepti_id = :resid AND NOT ainesosa_id = :ainid;").params(resid=resid, ainid=ainid)
            db.engine.execute(stmt)
        elif len(ainesosa_ids) == 2:
            ainid0 = str(ainesosa_ids[0])
            ainid1 = str(ainesosa_ids[1])
            stmt = text("DELETE FROM resepti_ainesosa WHERE resepti_id = :resid AND NOT ainesosa_id = :ainid0 AND NOT ainesosa_id =:ainid1;").params(resid=resid, ainid0=ainid0, ainid1=ainid1)
            db.engine.execute(stmt)
        elif len(ainesosa_ids) == 3:
            ainid0 = str(ainesosa_ids[0])
            ainid1 = str(ainesosa_ids[1])
            ainid2 = str(ainesosa_ids[2])
            stmt = text("DELETE FROM resepti_ainesosa WHERE resepti_id = :resid AND NOT ainesosa_id = :ainid0 AND NOT ainesosa_id =:ainid1 AND NOT ainesosa_id = :ainid2;").params(resid=resid, ainid0=ainid0, ainid1=ainid1, ainid2=ainid2)
            db.engine.execute(stmt)
    


class Resepti(Base):
    name = db.Column(db.String(144), nullable=False)
    cooktime = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    ohje_ref = db.relationship('Ohje', uselist=False, back_populates="resepti_ref", cascade="all, delete-orphan")

    ainesosa = db.relationship('Resepti_ainesosa', back_populates='resepti', cascade='all')

    def __init__(self, name, cooktime):
        self.name = name
        self.cooktime = cooktime

    @staticmethod
    def find_reseptit_with_arg_ainesosa(haettava):
        stmt = text("SELECT r.name, r.id FROM resepti r, ainesosa a, resepti_ainesosa i "
                    "WHERE r.id = i.resepti_id AND a.id = i.ainesosa_id AND a.name = :haettava;" ).params(haettava=haettava)

        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0], "id":row[1]})
        
        return response
    
    @staticmethod
    def find_resepti_ainesosa_count():
        stmt = text("SELECT resepti.name, COUNT(resepti_ainesosa.resepti_id) FROM resepti LEFT JOIN resepti_ainesosa ON resepti_ainesosa.resepti_id = resepti.id GROUP BY resepti.name;")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0], "amount":row[1]})
        print(response)
        return response


class Ainesosa(Base):
    name = db.Column(db.String(144), nullable=False)
    resepti = db.relationship('Resepti_ainesosa', back_populates='ainesosa', cascade='delete, delete-orphan')

    def __init__(self, name):
        self.name = name

    @staticmethod
    def find_ainesosat_for_recipe(recipe_id):
        stmt = text("SELECT a.name, i.amount FROM resepti r, ainesosa a, resepti_ainesosa i "
                    "WHERE r.id = i.resepti_id AND a.id =i.ainesosa_id AND r.id = :recipe_id ;").params(recipe_id=recipe_id)

        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0], "amount":row[1]})

        return response
    
    @staticmethod
    def clean_ainesosat():
        stmt = text("DELETE FROM ainesosa WHERE ainesosa.id NOT IN "
                "(SELECT resepti_ainesosa.ainesosa_id FROM resepti_ainesosa);")
        db.engine.execute(stmt)
 
    


        


    



