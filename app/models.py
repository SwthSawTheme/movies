from . import db

class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(255), nullable=False)
    video = db.Column(db.String(255), nullable=False)
