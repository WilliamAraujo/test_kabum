from flask_restful import Resource, reqparse
from models.product import ProductModel


class Products(Resource):
    def get(self):
        # SELECT * FROM produtos
        return {'produtos:': [product.json() for product in ProductModel.query.all()]}


class Product(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    atributos.add_argument('preco', type=float, required=True, help="The field 'preco' cannot be left blank.")
    atributos.add_argument('preco_prime', type=float)
    atributos.add_argument('preco_antigo', type=float)
    atributos.add_argument('disponibilidade', type=bool)
    atributos.add_argument('preco_desconto', type=float)
    atributos.add_argument('preco_desconto_prime', type=float)
    atributos.add_argument('link_descricao', type=str)
    atributos.add_argument('foto', type=str)
    atributos.add_argument('produto_prime', type=bool)

    def get(self, codigo):
        product = ProductModel.find_product(codigo)
        if product:
            return product.json()
        return {'message': 'Produto not found'}, 404 # not found

    def post(self, codigo):
        if ProductModel.find_product(codigo):
            return {"message": "Code '{}', produto already exists.".format(codigo)}, 400 #Bad Request
        data = Product.atributos.parse_args()
        product = ProductModel(codigo, **data)
        print("Produto: {}".format(product))
        try:
            product.save_product()
        except:
            return {"message": "An error ocurred trying to create produto."}, 500  # Internal Server Error
        return product.json(), 201

    def put(self, codigo):
        data = Product.atributos.parse_args()
        product_find = ProductModel.find_product(codigo)
        if product_find:
            product_find.update_product(**data)
            product_find.save_product()
            return product_find.json(), 200
        product = ProductModel(codigo, **data)
        product.save_product()
        return product.json(), 201

    def delete(self, codigo):
        product = ProductModel.find_product(codigo)
        if product:
            try:
                product.delete_product()
            except:
                return {'message': 'An error ocurre try to delete produto'}, 500
            return {'message': 'Produto deleted.'}
        return {'message': 'Produto not found.'}, 404


