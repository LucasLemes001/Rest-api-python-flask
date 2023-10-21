from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256   #Usar para Borrar o Password que o Cliente mandar a nós. Torna o que foi Passado a ele por letras e caracteres não legiveis
from flask_jwt_extended import create_access_token, jwt_required, get_jwt,create_refresh_token, get_jwt_identity
from db import db
from models import UserModel, BlocklistModel
from resources.schemas import UserSchemas, PlainBlocklistSchema

blp = Blueprint("Users","users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchemas)
    def post (self, user_data):
        if UserModel.query.filter(UserModel.username== user_data["username"]).first():
            abort(409, message="Já existe um usuário com esse username. Tente outro!!")
            
        new_user = UserModel(
            username= user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message":"Novo Usuário criado com sucesso!"}, 201
    
@blp.route("/user/<int:id_user>")
class User(MethodView):
    @blp.response(201, UserSchemas)
    def get(self, id_user):
        the_user = UserModel.query.get_or_404(id_user)
        return the_user
    
    @jwt_required()
    def delete(self, id_user):
        jwt = get_jwt()
        if not jwt.identity==1 :
            abort(401, message="You're not admin! Admin privilege required!")
        the_user = UserModel.query.get_or_404(id_user)
        db.session.delete(the_user)
        db.session.commit()

        return {"message":"Usuário foi deletado com sucesso!"}, 200
    


'''
        IMPORTANT NOTES ABOUT HEADERS AUTHENTICATES.
    * Using postman, to you dont make the authorization manually**
    1* SETA GLOBAL VARIABLE INSIDE POSTMAN
        
        1* bellow de endpoint, select "Tests" bar and set the 
        const response = pm.response.json()
        pm.globals.set("variable_name>", response.json_key_that_contain_the_jwt_value);
        2* Go on Auth bar, and select "Bearer Token".
        3* on the "Token" input digit {{jwt_token}} or the variable name.
        4* All endpoints that you want to protect, select the steps 2 and 3 again.
    
'''


@blp.route("/login")    
class Login(MethodView):
    @blp.arguments(UserSchemas)
    def post(self,user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            
            #USE TOKEN WITH ATRIBUTE "FRESH" IS IMPORTANT FOR CERTAIN ENDPOINTS, SUCH AS DELETE ACCONT OR EITHER DELETE ITENS, CHANGE PASSWORDS AND STUFFS
            #FOR REQUIRID FRESH TOKEN, CHECK THE "resources/itens.py" class ItemId/ def delete()
            access_token = create_access_token(identity=user.id, fresh=True)   
            refresh_token = create_refresh_token(identity=user.id)

            return {"access_token":access_token,"refresh_token":refresh_token}, 200
        
        abort(401, message="Credenciais Invalidas!")

'''
#Down here, the def will add the jwt that once belong to certain user
been added to a BLOCKLIST, wich means that when someone click on logout, he's token is ganna blockhim to access some endpoint
 been obligde to login again. This is very usefull if some one left her machine and leaves de aplication website opened.
 Protecting clients having their accont bullyed(specially if the user are a admin).
 
 #Abaixo, a def vai adicionar o jwt que uma vez pertenceu a algum usuario e adicionar a um banco de dados
 e na pratica isso quer dizer que sempre que a pesoa clicar no Logout, seu token se tornara invalido, forçanco a pessoa
 a logar de volta para acessar certos endpoints. Isso é especialmente necessario para que a o client nao tenha sua
 conta violada caso esse deixe a Api aberta no computador. (Especialmente se ela for um admin)'''




@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(Self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return{"access_token":new_token}



@blp.route("/logout")
class Logout(MethodView):
   
    @jwt_required()
    @blp.response(201, PlainBlocklistSchema)
    def post(self):
        jti = get_jwt()["jti"]
        new_revoked_token = BlocklistModel(
            revoked_token = jti
        )
        db.session.add(new_revoked_token)
        db.session.commit()
        
        
        return {"message":"Logout success!"}

def check_jwt_in_blocklist():
    pass