from db import db 

class TagModel(db.Model):
    
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(80), unique=False,nullable= False)
    id_loja = db.Column(db.Integer,db.ForeignKey("lojas.id"),nullable=False)

    loja = db.relationship("LojasModelo", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
    