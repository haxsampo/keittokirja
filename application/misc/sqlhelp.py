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

class startupInsertionContainer():
    @staticmethod
    def insert_test_accounts():
        stmt = text("INSERT INTO account (username, name, password, user_group) "
                    "VALUES ('', '', '', 0);")

        db.engine.execute(stmt)

    @staticmethod
    def insert_test_recipes():
        stmt = text("INSERT INTO resepti (name, cooktime, account_id) VALUES ('nakkivanukas', '120', '1');")
        stmt1 = text("INSERT INTO resepti (name, cooktime, account_id) VALUES ('nakkikakku', '33', '1');")
        db.engine.execute(stmt)
        db.engine.execute(stmt1)

        stmt = text("INSERT INTO ainesosa (name) VALUES ('nakki');")
        stmt1 = text("INSET INTO ainesosa(name) VALUES ('jauho');")
        stmt2 = text("INSET INTO ainesosa(name) VALUES ('vanukas');")
        db.engine.execute(stmt)
        db.engine.execute(stmt1)
        db.engine.execute(stmt2)

        stmt = text("INSERT INTO resepti_ainesosa (resepti_id, ainesosa_id, amount) VALUES ('1', '1','1');")
        stmt1 = text("INSERT INTO resepti_ainesosa (resepti_id, ainesosa_id, amount) VALUES ('1', '3','2');")
        stmt2 = text("INSERT INTO resepti_ainesosa (resepti_id, ainesosa_id, amount) VALUES ('2', '1','3');")
        stmt3 = text("INSERT INTO resepti_ainesosa (resepti_id, ainesosa_id, amount) VALUES ('2', '2','4');")
        db.engine.execute(stmt)
        db.engine.execute(stmt1)
        db.engine.execute(stmt2)
        db.engine.execute(stmt3)