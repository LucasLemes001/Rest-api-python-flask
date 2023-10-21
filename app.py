import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from sqlalchemy import desc
from models import BlocklistModel

from resources.items import blp as ItemBlueprint
from resources.lojas import blp as LojasBlueprint
from resources.tags import blp as TagBlueprint
from resources.users import blp as UserBlueprint

def create_app(db_url=None):
    app = Flask(__name__)


    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Lojas REST API"
    app.config["API_VERSION"] ="v1"
    app.config["OPENAPI_VERSION"] ="3.0.3"
    app.config["OPENAPI_URL_PREFIX"]="/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]="/swagger-ui"  #http://127.0.0.1:5000/swagger-ui
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
    db.init_app(app)
    migrate = Migrate(app, db)

    api= Api(app)
    app.config["JWT_SECRET_KEY"] = "213215336955569235321822625467491083"
    jwt = JWTManager(app)
    @jwt.additional_claims_loader
    def additional_claims_to_jwt(identity):
        # Look into the detabse and see whether the user is an admin
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
        
    
    '''#TODA VEZ QUE RECEBE-SE UM TOKEN,
    ESSA FUNÇÃO RODA, E SE ELA RETORNA "TRUE", O CLIENTE RECEBE UM ERRO, "TOKEN NOT AVALIABLE". 
    DEFINIMOS QUAL ERRO EM ESPECÍFICO COM UMA OUTRA FUNÇÃO'''
    @jwt.token_in_blocklist_loader    
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        jti = jwt_payload["jti"]  # Here we fucking extract the JTI file in the persons Tokens.
        
        # Tenho que Fazer ele checar no banco de dados Se existe um JTI que o cliente esta usando atualmente
        # Check into de Db if there's a JTI that has been revoked and still been used.
       
        #DOWN HERE HE CATCH THE DATA FROM BLOCKLIST TABLE AS A <LIST> ('jtinumber',) <len 1>
        blocked_tokens = BlocklistModel.query.with_entities(BlocklistModel.revoked_token).order_by(desc(BlocklistModel.id)).all()
        for blocked_token in blocked_tokens:  # this loop search in the list, the indicies [0](jti number) and check if the jti isn't in the BLOCKLIST.DB table
            if blocked_token[0] in jti: return True #IF jti if found on the BLOCKLIST table and still find in client header, so we return True for an Error treatment.

        
        
    
    '''
    #DEFININDO UMA FUNÇÃO QUE VAI RETORNAR O ERRO PARA O CLIENT QUANDO A FUNÇÃO ACIMA RETORNA "TRUE".
    QUAL ERRO EM EPECÍFICO O CLIENTE RECEBE SE O TOKEN
    ESTIVER SIDO NEGADO
    '''
    @jwt.revoked_token_loader
    def revoked_token(jwt_header,jwt_payload):
        return(
            jsonify(
                {"descrition":"The Token has been revoked.","error":"token_revoked"}
            )
        ), 401
    
    
    '''
    # AQUI ABAIXO, CRIAR 3 FUNÇOES... 
    1. Quando o token jwt expira, 
    2. quando o token é inválido, pq o cliente tentou modidica-lo, 
    3. Quando ele NÃO tem um jwt
    4. Quando espera um Fresh_Token
    '''

    @jwt.expired_token_loader   #Esses "@" antes o jwt.<erro> são necessários para chamar a funçção caso o determinado erro venha a surgir
    def expired_jwt_error(jwt_header,jwt_payload):
        return (
            jsonify({"message":"Seu Token foi expirado! Deverá refazer o login!","error":"expired_jwt_error!"})
        ), 401
    
    @jwt.invalid_token_loader    
    def invalid_token_error(error):
        return (
            jsonify(
                {"message":"Falha na Verificação!","error":"invalid_token"}
            )
        ),401
    @jwt.unauthorized_loader
    def missing_token_error(error):
        return(
            jsonify(
                {"message":"Você ainda não fez login! Faça Login para prosseguir!","error":"missing_token"}
            )
        ),401

    @jwt.needs_fresh_token_loader
    def not_fresh_token_callback(jwt_header,jwt_payload):
        return(
            jsonify(
                {
                    "descrition":"The token is not Fresh.",
                    "error":"fresh_token_required"
                }
            )
        ), 401
    
    
    
   #Since we are using flask-migrate, Migrate()  to create de Db, we no longer need to SQLAlchemy to doing so....
   #Since we will be using Flask-Migrate to create our database, we no longer need to tell Flask-SQLAlchemy to do it when we create the app.
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(LojasBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
