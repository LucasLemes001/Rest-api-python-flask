from flask.views import MethodView
from flask_smorest import Blueprint,abort
from models import LojasModelo
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt
from resources.schemas import LojaSchema
'''
>>>>>>>     Uma observação importante       <<<<<<
Nessa variável abaixo que está herdando toda a Classe Blueprint, em seu primeiro argumento, deverá ser a "base"
de todos os endpoints como nos exemplos abaixo
blp.route("/'nome que vc der',__name__, descriotion='Descricão de com O QUE você está trabalhando'")
Caso contrario, não ira funcionar'''

blp = Blueprint("lojas", __name__,description ="Operando Lojas")


@blp.route("/lojas/<string:id_loja>")
class LojasID(MethodView):
    
    @blp.response(200, LojaSchema)
    def get(self, id_loja):
        loja = LojasModelo.query.get_or_404(id_loja)
        return loja
    
    @jwt_required(fresh=True)
    def delete(self,id_loja):
        jwt = get_jwt()
        if not jwt.identity == "is_admin":
            abort(401, message="You're not an Admin! Admin privilege required!")

        loja = LojasModelo.query.get_or_404(id_loja)
        db.session.delete(loja)
        db.session.commit()
        return {"Message":"Loja Deletada com Sucesso!"}, 200
    


@blp.route("/lojas")
class Lojas(MethodView):

    @blp.response(200, LojaSchema(many=True))
    def get(self):
        return LojasModelo.query.all()
    
    @jwt_required()
    @blp.arguments(LojaSchema)
    @blp.response(201, LojaSchema)
    def post(self, dados):
        
        nova_loja = LojasModelo(**dados)
        try:
            db.session.add(nova_loja)
            db.session.commit()
        
        
        except IntegrityError:
            abort(400, message=f"Erro ao criar nova Loja. Esse nome de loja já existe")
        
        
        except SQLAlchemyError:
            abort(500, message=f"Occoreu um erro ao CRIAR uma NOVA LOJA")

        return nova_loja
    




    