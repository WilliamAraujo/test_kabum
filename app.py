import os
from flask import Flask
from flask_restful import Api
from utils.process import Process
from models.product import ProductModel
from resources.product import Products, Product
from utils.config_helper import ConfigHelper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_database():
    if not os.path.exists('./database.db'):
        print("Create a database\n")
        database.create_all()

    file_name = "produtos_79936.json"
    if not os.path.exists(file_name):
        print("Download of mock database\n")
        Process.run('curl https://servicespub.prod.api.aws.grupokabum.com.br/descricao/v1/descricao/produto/79936 >> %s' % file_name)

    print("Save database")
    # Read $filename
    config_file = './%s' % file_name
    config_helper = ConfigHelper(config_file)
    config = config_helper.load_config()

    # Read only 'produtos'
    config = config['familia']['produtos']
    for data in config:
        print("data: {}\n\n".format(data))
        product = ProductModel(**data)
        try:
            product.save_product()
        except:
            print({"message": "An error ocurred trying to create 'produto'."}, 500)  # Internal Server Error
        print(product.json(), 201)

api.add_resource(Products, '/produto')
api.add_resource(Product, '/produto/<int:codigo>')


if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)
