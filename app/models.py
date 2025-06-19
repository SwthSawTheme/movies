from . import db

class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(255), nullable=False)
    video = db.Column(db.String(255), nullable=False)
    colecao_id = db.Column(db.Integer, db.ForeignKey("colecao.id"), nullable=True)

class Colecao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    imagem = db.Column(db.String(255), nullable=True)
    filmes = db.relationship("Filme", backref="colecao", lazy=True)
