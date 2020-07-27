from sql_alchemy import database


class ProductModel(database.Model):

    __tablename__ = 'products'

    codigo = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(80))
    preco = database.Column(database.Float(precision=2))
    preco_prime = database.Column(database.Float(precision=1))
    preco_antigo = database.Column(database.Float(precision=1))
    disponibilidade = database.Column(database.Boolean)
    preco_desconto = database.Column(database.Float(precision=1))
    preco_desconto_prime = database.Column(database.Float(precision=1))
    link_descricao = database.Column(database.String(200))
    foto = database.Column(database.String(200))
    produto_prime = database.Column(database.Boolean)

    def __init__(self, codigo=None, nome=None, preco=None, preco_prime=None, preco_antigo=None, disponibilidade=False,
                 preco_desconto=None, preco_desconto_prime=None, link_descricao=None, foto=None, produto_prime=False):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.preco_prime = preco_prime
        self.preco_antigo = preco_antigo
        self.disponibilidade = disponibilidade
        self.preco_desconto = preco_desconto
        self.preco_desconto_prime = preco_desconto_prime
        self.link_descricao = link_descricao
        self.foto = foto
        self.produto_prime = produto_prime

    def json(self):
        return {
            'codigo': self.codigo,
            'nome': self.nome,
            'preco': self.preco,
            'preco_prime': self.preco_prime,
            'preco_antigo': self.preco_antigo,
            'disponibilidade': self.disponibilidade,
            'preco_desconto': self.preco_desconto,
            'preco_desconto_prime': self.preco_desconto_prime,
            'link_descricao': self.link_descricao,
            'foto': self.foto,
            'produto_prime': self.produto_prime
        }

    @classmethod
    def find_product(cls, codigo):
        product = cls.query.filter_by(codigo=codigo).first()
        if product:
            return product
        return None

    def save_product(self):
        database.session.add(self)
        database.session.commit()

    def update_product(self, nome=None, preco=None, preco_prime=None, preco_antigo=None, disponibilidade=False,
        preco_desconto=None, preco_desconto_prime=None, link_descricao=None, foto=None, produto_prime=False):
        self.nome = nome
        self.preco = preco
        self.preco_prime = preco_prime
        self.preco_antigo = preco_antigo
        self.disponibilidade = disponibilidade
        self.preco_desconto = preco_desconto
        self.preco_desconto_prime = preco_desconto_prime
        self.link_descricao = link_descricao
        self.foto = foto
        self.produto_prime = produto_prime

    def delete_product(self):
        database.session.delete(self)
        database.session.commit()