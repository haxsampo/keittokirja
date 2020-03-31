from application import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

class requestContainer():
    @staticmethod
    def find_ainesosat_for_resepti(resepti_id):
        stmt = text("SELECT a.name, a.id FROM resepti r, ainesosa a, resepti_ainesosa i "
                    "WHERE r.id = i.resepti_id AND a.id =i.ainesosa_id AND r.id = " + 
                    resepti_id +";")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0], "id":row[1]})
        
        return response
