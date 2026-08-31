from app import db

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Numeric(10, 2), default=0)
    duration_min = db.Column(db.Integer, default=30)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
