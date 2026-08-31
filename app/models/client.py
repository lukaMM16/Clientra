from app import db

class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    

