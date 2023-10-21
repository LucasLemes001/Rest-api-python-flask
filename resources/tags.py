
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, LojasModelo, ItemModel
from resources.schemas import TagSchema, TagAndItemSchema


blp = Blueprint("Tags","tags", description="Operando Tags")

@blp.route("/loja/<string:id_loja>/tag")   # http://127.0.0.1:5000/loja/<string:id_loja>/tag   #BUSCAR NA LOJA X A TAG X
class TagsInLoja(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, id_loja):
        loja = LojasModelo.query.get_or_404(id_loja)
        
        return loja.tags.all()
    # AQUI ELE PEGA TODAS AS TAGS DA LOGA ESPECIFICA.
    
    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(self, tag_data, id_loja):
        if TagModel.query.filter(TagModel.id_loja==id_loja, TagModel.nome == tag_data["nome"]).first():
            abort(400, message=f"Uma Tag com esse Nome Ja EXISTE Nesta Loja!")
        
        tag = TagModel(**tag_data, id_loja=id_loja)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as erro:
            abort(500, message=str(erro))

        return tag

 
@blp.route("/item/<string:id_item>/tag/<string:id_tag>")    #http://127.0.0.1:5000/item/id_iem/tag/id_tag   #LIGAR AO ITEM X A TAG X
class LinkTagtoItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self,id_item, id_tag):
        item = ItemModel.query.get_or_404(id_item)
        tag = TagModel.query.get_or_404(id_tag)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Um erro occoreu ao Inserir Tag à um Item")    

        return tag
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, id_item, id_tag):   ##http://127.0.0.1:5000/item/id_item/tag/id_tag   DELETAR DO ITEM X A TAG X
        item = ItemModel.query.get_or_404(id_item)
        tag = TagModel.query.get_or_404(id_tag)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Occorreu um erro ao deletar uma tag de um item")
        
        return {"Mensagem": "Um Item foi removida de uma Tag", "Item":item,"Tag":tag }
    
    

@blp.route("/tag/<string:id_tag>")   
class Tag(MethodView):
    @blp.response(200, TagSchema)  
    def get(self, id_tag):    #http´://127.0.0.1:5000/tag/id_tag   #Buscar toda info da Tag X
        tag = TagModel.query.get_or_404(id_tag)
        return tag
    
    @blp.response(
        202,
        description="Deletar uma tag se não houver Items Ligados a Ela",
        example={"Mensage":"Tag deletada"},
    )
    @blp.alt_response(404, description="Tag Não encontrada")
    @blp.alt_response(
        400, 
        description="Retornar se a Tag está ligada a um ou mais items, nesse caso a Tag não foi Excluida"
        
    )
    def delete(self, id_tag):   #http://127.0.0.1:5000/tag/id_tag # Dell tag com ID X se ela nao estiver linkada a um item
        tag = TagModel.query.get_or_404(id_tag)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"Mensagem":"Tag Excluida"}
        abort (404, Message ="Não foi Possivel deletar a Tag. Tenha certeza de que a Tag não está ligada a nenhum item!!")
        

