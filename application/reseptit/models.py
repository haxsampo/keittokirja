from application import db

class Resepti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    nimi = db.Column(db.String(144), nullable=False)
    valmistusaika = db.Column(db.Integer, nullable=False)
    hinta = db.Column(db.Integer, nullable=False)

    def __init__(self, nimi, valmistusaika, hinta):
        self.nimi = nimi
        self.valmistusaika = valmistusaika
        self.hinta = hinta
