from application import db
from application.models import Base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


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