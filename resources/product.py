from flask_restful import Resource, reqparse
from models.product import ProductModel


class Products(Resource):
    def get(self):
        # SELECT * FROM products
        return {'products:': [product.json() for product in ProductModel.query.all()]}


class Product(Resource):
    attribute = reqparse.RequestParser()
    attribute.add_argument('nome', type=str, required=True, help="The field name cannot be left blank.")
    attribute.add_argument('preco', type=float, required=True, help="The field 'preco' cannot be left blank.")
    attribute.add_argument('preco_prime', type=float)
    attribute.add_argument('preco_antigo', type=float)
    attribute.add_argument('disponibilidade', type=bool)
    attribute.add_argument('preco_desconto', type=float)
    attribute.add_argument('preco_desconto_prime', type=float)
    attribute.add_argument('link_descricao', type=str)
    attribute.add_argument('foto', type=str)
    attribute.add_argument('produto_prime', type=bool)

    def get(self, codigo):
        product = ProductModel.find_product(codigo)
        if product:
            return product.json()
        return {'message': 'Product not found'}, 404 # not found

    def post(self, codigo):
        if ProductModel.find_product(codigo):
            return {"message": "Code '{}', product already exists.".format(codigo)}, 400 # Bad Request
        data = Product.attribute.parse_args()
        product = ProductModel(codigo, **data)
        try:
            product.save_product()
        except:
            return {"message": "An error ocurred trying to create product."}, 500  # Internal Server Error
        return product.json(), 201

    def put(self, codigo):
        data = Product.attribute.parse_args()
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
                return {'message': 'An error ocurre try to delete product'}, 500
            return {'message': 'Product deleted.'}
        return {'message': 'Product not found.'}, 404


