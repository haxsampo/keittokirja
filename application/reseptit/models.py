from application import db
from application.models import Base

class Resepti(Base):

    name = db.Column(db.String(144), nullable=False)
    cooktime = db.Column(db.Integer, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, name, cooktime):
        self.name = name
        self.cooktime = cooktime
