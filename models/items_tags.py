from db import db

class ItemsTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    id_item = db.Column(db.Integer, db.ForeignKey("items.id"))
    id_tag = db.Column(db.Integer, db.ForeignKey("tags.id"))



