from application import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


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