from application import db
from application.models import Base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table

#Ainesosa-Resepti assosiaatiotaulu
resepti_ainesosa = db.Table('resepti_ainesosa',
                    db.Column('resepti_id', db.Integer, db.ForeignKey('resepti.id')),
                    db.Column('ainesosa_id', db.Integer, db.ForeignKey('ainesosa.id'))
                    )

class Resepti(Base):

    name = db.Column(db.String(144), nullable=False)
    cooktime = db.Column(db.Integer, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    ainesosa = db.relationship('Ainesosa', 
                            secondary=resepti_ainesosa, 
                            back_populates='resepti')

    def __init__(self, name, cooktime):
        self.name = name
        self.cooktime = cooktime



class Ainesosa(Base):
    name = db.Column(db.String(144), nullable=False) #lisää tälle unique=True kun on tunkattu
    resepti = db.relationship('Resepti', 
                            secondary=resepti_ainesosa, 
                            back_populates='ainesosa')

    def __init__(self, name):
        self.name = name




