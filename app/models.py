from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

    #Relacionamentos
    transacoes = db.relationship('Transacao', backref='usuario', lazy=True)
    categorias = db.relationship('Categoria', backref='usuario', lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    



class Transacao(db.Model):
    __tablename='transacoes'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'Receita' ou 'Despesa'
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)

    #Relacionamento
    categoria = db.relationship('Categoria', backref= 'transacoes')

class Categoria (db.Model):
    id =db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50), nullable = False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)

    def __repr__(self):
        return f"<Categoria {self.nome}>"