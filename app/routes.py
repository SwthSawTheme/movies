from flask import Blueprint, render_template, request, redirect, url_for
from .models import Filme
from . import db
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
from .models import Filme, Colecao
from flask import send_file
import mimetypes

routes = Blueprint('routes', __name__)

@routes.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    filmes = Filme.query.filter(Filme.colecao_id == None)\
        .order_by(Filme.id.desc())\
        .paginate(page=page, per_page=4)
    return render_template('index.html', filmes=filmes)


@routes.route("/assistir/<int:filme_id>")
def assistir(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    return render_template("assistir.html", filme=filme)

@routes.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    colecoes = Colecao.query.all()
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        imagem = request.form["imagem"]
        video = request.form["video"]
        colecao_id = request.form.get("colecao_id") or None

        novo_filme = Filme(
            titulo=titulo,
            descricao=descricao,
            imagem=imagem,
            video=video,
            colecao_id=colecao_id
        )
        db.session.add(novo_filme)
        db.session.commit()
        return redirect(url_for("routes.home"))
    return render_template("adicionar.html", colecoes=colecoes)

@routes.route("/editar/<int:filme_id>", methods=["GET", "POST"])
def editar(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    colecoes = Colecao.query.all()
    if request.method == "POST":
        filme.titulo = request.form["titulo"]
        filme.descricao = request.form["descricao"]
        filme.imagem = request.form["imagem"]
        filme.video = request.form["video"]
        filme.colecao_id = request.form.get("colecao_id") or None
        db.session.commit()
        return redirect(url_for("routes.home"))
    return render_template("editar.html", filme=filme, colecoes=colecoes)


@routes.route("/remover/<int:filme_id>")
def remover(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    db.session.delete(filme)
    db.session.commit()
    return redirect(url_for("routes.home"))


@routes.route('/media/video/<int:filme_id>')
def servir_video(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    if not os.path.exists(filme.video):
        return f"Vídeo não encontrado: {filme.video}", 404

    tipo_mime, _ = mimetypes.guess_type(filme.video)
    return send_file(filme.video, mimetype=tipo_mime or 'application/octet-stream')


@routes.route('/media/imagem/<int:filme_id>')
def servir_imagem(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    return send_file(filme.imagem, mimetype='image/jpeg')

@routes.route("/colecoes")
def listar_colecoes():
    page = request.args.get("page", 1, type=int)
    per_page = 4
    colecoes = Colecao.query.paginate(page=page, per_page=per_page)
    return render_template("colecoes.html", colecoes=colecoes)

@routes.route('/colecao/<int:colecao_id>/assistir_todos')
def assistir_todos(colecao_id):
    colecao = Colecao.query.get_or_404(colecao_id)
    filmes_serializaveis = [
        {'id': f.id, 'titulo': f.titulo} for f in colecao.filmes
    ]
    return render_template('assistir_todos.html', colecao=colecao, filmes=filmes_serializaveis)

@routes.route("/colecao/<int:colecao_id>")
def ver_colecao(colecao_id):
    colecao = Colecao.query.get_or_404(colecao_id)
    filmes_ordenados = sorted(colecao.filmes, key=lambda f: f.id)
    return render_template('colecao.html', colecao=colecao, filmes=filmes_ordenados)

@routes.route("/colecao/adicionar", methods=["GET", "POST"])
def adicionar_colecao():
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        imagem = request.form["imagem"]

        nova_colecao = Colecao(nome=nome, descricao=descricao, imagem=imagem)
        db.session.add(nova_colecao)
        db.session.commit()
        return redirect(url_for("routes.listar_colecoes"))
    return render_template("adicionar_colecao.html")

@routes.route('/editar_colecao/<int:colecao_id>', methods=['GET', 'POST'])
def editar_colecao(colecao_id):
    colecao = Colecao.query.get_or_404(colecao_id)

    if request.method == 'POST':
        colecao.titulo = request.form['titulo']
        colecao.descricao = request.form['descricao']
        colecao.imagem = request.form['imagem']  # Caminho direto no PC

        db.session.commit()
        return redirect(url_for('routes.listar_colecoes'))

    return render_template('editar_colecao.html', colecao=colecao)


@routes.route("/media/imagem_colecao/<int:colecao_id>")
def servir_imagem_colecao(colecao_id):
    colecao = Colecao.query.get_or_404(colecao_id)
    if not os.path.exists(colecao.imagem):
        return f"Imagem da coleção não encontrada: {colecao.imagem}", 404
    return send_file(colecao.imagem, mimetype="image/jpeg")
