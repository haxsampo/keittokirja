from application import db
from application.models import Base
from application.reseptit.models import Resepti
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

class Ohje(Base):
    ohjeet = db.Column(db.Text)
    resepti_id = db.Column(db.Integer, db.ForeignKey('resepti.id'))
    resepti_ref = db.relationship("Resepti", back_populates="ohje_ref", lazy=True)

    def __init__(self, ohje):
        self.ohjeet = ohje

    @staticmethod
    def find_ohje_with_id(resepti_id):
        stmt = text("SELECT ohjeet FROM ohje WHERE resepti_id = :resepti_id;").params(resepti_id=resepti_id)

        res = db.engine.execute(stmt)  
        response = []
        for row in res:
            response.append({"rivi":row[0]})

        try:
            pal = response[0]['rivi'].split("\r\n")
        except:
            pal = response[0]['rivi']
        #pal = response[0]['rivi']
        print(type(pal))
        print(pal)
        return pal