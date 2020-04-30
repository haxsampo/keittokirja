from application import db
from application.models import Base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


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

 
    


        


    



