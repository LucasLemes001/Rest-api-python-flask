from marshmallow import Schema,fields


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    preco = fields.Float(required=True)


class PlainLojaSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str()


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str()


class ItemUpdadeSchema(Schema):
    nome = fields.Str()
    preco = fields.Float()




class ItemSchema(PlainItemSchema):
    id_loja = fields.Int(required=True, load_only=True)
    loja = fields.Nested(PlainLojaSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)


class TagSchema(PlainTagSchema):
    id_loja = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    loja = fields.Nested(PlainLojaSchema(),dump_only=True)


class LojaSchema(PlainLojaSchema):
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))
    tags =fields.List(fields.Nested(PlainTagSchema()),dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
    

class UserSchemas(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)  #NUNCA RETORNAR O PASSWORD PARA O CLIENT


class PlainBlocklistSchema(Schema):
    id = fields.Integer(dump_only=True)
    revoked_token = fields.Str(required=True, load_only=True)

    
    



