from flask_restful import Resource, reqparse
from models.produto import ProdutoModel


class Produtos(Resource):
    def get(self):
        # SELECT * FROM produtos
        return {'produtos:': [produto.json() for produto in ProdutoModel.query.all()]}


class Produto(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    atributos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank.")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, produto_id):
        produto = ProdutoModel.find_produto(produto_id)
        if produto:
            return produto.json()
        return {'message': 'Product not found'}, 404 # not found

    def post(self, produto_id):
        if ProdutoModel.find_produto(produto_id):
            return {"message": "Produto id '{}' already exists.".format(produto_id)}, 400 #Bad Request
        dados = Produto.atributos.parse_args()
        produto = ProdutoModel(produto_id, **dados)
        try:
            produto.save_produto()
        except:
            return {"message": "An error ocurred trying to create product."}, 500  # Internal Server Error
        return produto.json(), 201

    def put(self, produto_id):
        dados = Produto.atributos.parse_args()
        produto_encontrado = ProdutoModel.find_produto(produto_id)
        if produto_encontrado:
            produto_encontrado.update_hotel(**dados)
            produto_encontrado.save_hotel()
            return produto_encontrado.json(), 200
        produto = ProdutoModel(produto_id, **dados)
        produto.save_produto()
        return produto.json(), 201

    def delete(self, produto_id):
        produto = ProdutoModel.find_produto(produto_id)
        if produto:
            try:
                produto.delete_produto()
            except:
                return {'message': 'An error ocurre try to delete produto'}, 500
            return {'message': 'Produto deleted.'}
        return {'message': 'Produto not found.'}, 404


