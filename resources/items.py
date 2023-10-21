from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel
from resources.schemas import ItemSchema, ItemUpdadeSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt


'''
>>>>>>>     Uma observação importante       <<<<<<
Nessa variável abaixo que está herdando toda a Classe Blueprint, em seu primeiro argumento, deverá ser a "base"
de todos os endpoints como nos exemplos abaixo
blp.route("/'nome que vc der',__name__, descriotion='Descricão de com O QUE você está trabalhando'")
Caso contrario, não ira funcionar'''

blp = Blueprint("items",__name__, description= "Operando Items")

@blp.route("/items/<string:id_item>")
class ItemsID(MethodView):
    
    @blp.response(200, ItemSchema)
    def get(self, id_item):
        item = ItemModel.query.get_or_404(id_item)
        return item
    
    @jwt_required(fresh=True)  #WHEN YOU PUT THE "FRESH" PARAMETHER, THE USER MUST CARRY WITH HIM A FRESH TOKEN, NEEDING TO LOG IN AGAIN IF HE HAVEN'T ONE
    def delete(self, id_item):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        item = ItemModel.query.get_or_404(id_item)
        db.session.delete(item)
        db.session.commit()
        return {"Message":"Item Deletado com Sucesso!"}, 200
        
    
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemUpdadeSchema)
    @blp.response(200, ItemUpdadeSchema)
    def put(self, dados_item, id_item):
        item_atualizado = ItemModel.query.get(id_item)
        if item_atualizado:
            item_atualizado.preco = dados_item["preco"]
            item_atualizado.nome = dados_item["nome"]
        

        else:
            item_atualizado = ItemModel(id=id_item, **dados_item)
        
        db.session.add(item_atualizado)
        db.session.commit()

        return item_atualizado
        




@blp.route("/items")
class Items(MethodView):
    
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, dados):
        
        item = ItemModel(**dados)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message=f"Um erro ocorreu ao CRIAR um ITEM!")

        return item
