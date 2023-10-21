from flask import Flask,request
from db import items,lojas
import uuid
from flask_smorest import abort

app = Flask(__name__)



#                >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>           LOJA        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


@app.get("/")   # >>>> RECOLHER TODAS AS LOJAS    <<<<
def ObeterLojas():
    return {"Lojas": list(lojas.values())}  # SE NAO CONVERTER OS VALORES EM LISTA ANTES, NÃO CONSEGUIMOS RECEBE-LOS COMO JSON


@app.get("/loja/<string:id_loja>")  # >>> RECOLHER LOJA ESPECÍFICA <<<
def obterInfoLoja_ID(id_loja):
    try:
        return lojas[id_loja]
    except KeyError:
        abort(404, message=f"Loja não Encontrada! =(")

    
@app.post("/criandonovaloja")    #>>>>>>   CRIAR NOVA LOJA <<<<
def CriarNovaLoja():
    receber_dados = request.get_json()
    if "nome" not in receber_dados:
        abort(400, message=f"Bad Request. Certifíque-se de há 'nome' na loja que estamos adicionando!!")
    for loja in lojas.values():
        if receber_dados["nome"] == loja["nome"]:
            abort(400, message=f"Essa loja Já Existe!!")


        
    loja_id = uuid.uuid4().hex    #Gerar IDS nao repetidos SIMULANDO BANCO DE DADOS!!!
    nova_loja = {**receber_dados,"id":loja_id }
    lojas[loja_id] = nova_loja  # Como a Variavel Lojas é um dict, ele não precisa de um APPEND, basta um sinal de "=" para receber as novas informações
    return nova_loja, 201


@app.delete("/loja/<string:id_loja>") # >>> DELETAR LOJA POR ID <<<
def DeletarLoja(id_loja):
    try:
        del lojas[id_loja]
        return {"Message":"Loja Excluída com sucesso!"}
    except KeyError:
        abort(400, messege=f"Erro ao Excluir Loja! Id_Loja não encontrado!!!")







#                >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>          ITEMS        <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<                 



@app.get("/item")    # >>> RECOLHER TODOS OS ITEMS <<<<
def Obeteritems():
    return {"items": list(items.values())}  # SE NAO CONVERTER OS VALORES EM LISTA ANTES, NÃO CONSEGUIMOS RECEBE-LOS COMO JSON


@app.get("/item/<string:id_item>")  # >>> RECOLHER ITEM ESPECIFICO <<<
def obterItemId(id_item):
    try:
        return items[id_item]
    except KeyError:
        abort(404, message=f"Item não Encontrada! =(")
    

@app.post("/novoitem")    # >>> CRIAR NOVO ITEM <<< 
def NovoItem():
    dadosDoIten = request.get_json()
    if (
        "nome" not in dadosDoIten 
        or "preco" not in dadosDoIten 
        or "id_loja" not in dadosDoIten
    ):
        abort(400, message="Bad request. Pode estar faltando um ou mais dos seguinte dados:(nome,preco ou id_loja)")
    
    for item in items.values():
        if (
            dadosDoIten["nome"] == item["nome"]
            and dadosDoIten["id_loja"] == item["id_loja"]
        ):
            abort(400, message=f"Item ja Existente.")
        

    
    id_item = uuid.uuid4().hex
    novo_item = {**dadosDoIten,"id":id_item}
    items[id_item] = novo_item   # >>>  ISSO AQUI DUE MOH TRAMPO PORQUE DENTRO DO ITEM[ID_ITEM] ESTAVA FAZENDO ITEM["ID_ITEM"]. Tentava add à uma chave não existente, ao invez de acrescentar mais um dict <<<<<
    
    return novo_item

@app.delete("/item/<string:id_item>")
def DeletarItem(id_item):
    try:
        del items[id_item]
        return {"Message": "Item exlcuído com sucesso!"}
    except KeyError:
        abort(404, message=f"Item não econtrado! Falha ao deletar")


@app.put("/item/<string:id_item>")
def ModificarItem(id_item):
    dados = request.get_json()
    if (
        "nome" not in dados
        and "preco" not in dados
    ):
        abort(400, message="Bad request. Tenha certeza de que há nome ou preco para alterar")
    
    a = items[id_item]
    modificacao = {**a,**dados}
    items[id_item]= modificacao
    return {"mensagem":"Item modificado"}
