from application import db
from application.models import Base

class User(Base):
    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    user_group = db.Column(db.Integer, nullable=False) #0 = admin

    reseptit = db.relationship("Resepti", backref='account', lazy=True)

    def __init__(self, name, username, password, user_group):
        self.name = name
    
    def get_id(self):
        return self.id

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True