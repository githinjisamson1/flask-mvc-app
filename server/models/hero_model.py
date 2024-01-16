from app import db
from sqlalchemy_serializer import SerializerMixin


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heropowers = db.relationship("HeroPower", backref="hero")
    # powers = db.relationship("HeroPower", back_populates="powers")

    # what to exclude hence prevent recursion
    serialize_rules = ("-heropowers.hero",)

    def __repr__(self):
        return f'''Hero {self.name} {self.super_name}'''
