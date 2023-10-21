from db import db

class ItemModel(db.Model):

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=False, nullable=False)
    preco = db.Column(db.Float(precision=2), unique=False, nullable=False)
    description = db.Column(db.String())
    
    
    id_loja = db.Column(db.Integer,db.ForeignKey("lojas.id"),unique=False,nullable=False)
    
    loja = db.relationship("LojasModelo", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
    