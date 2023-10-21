from db import db

class LojasModelo(db.Model):

    __tablename__ = "lojas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    items = db.relationship("ItemModel", back_populates="loja", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="loja", lazy="dynamic")

    