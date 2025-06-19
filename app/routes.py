from flask import Blueprint, render_template, request, redirect, url_for
from .models import Filme
from . import db
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
from .models import Filme
from flask import send_file
import mimetypes

routes = Blueprint('routes', __name__)

@routes.route("/")
def home():
    filmes = Filme.query.all()
    return render_template("index.html", filmes=filmes)

@routes.route("/assistir/<int:filme_id>")
def assistir(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    return render_template("assistir.html", filme=filme)

@routes.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        imagem_path = request.form["imagem"]  # Caminho absoluto
        video_path = request.form["video"]    # Caminho absoluto

        novo_filme = Filme(
            titulo=titulo,
            descricao=descricao,
            imagem=imagem_path,
            video=video_path
        )
        db.session.add(novo_filme)
        db.session.commit()

        return redirect(url_for("routes.home"))

    return render_template("adicionar.html")

@routes.route("/editar/<int:filme_id>", methods=["GET", "POST"])
def editar(filme_id):
    filme = Filme.query.get_or_404(filme_id)
    if request.method == "POST":
        filme.titulo = request.form["titulo"]
        filme.descricao = request.form["descricao"]
        filme.imagem = request.form["imagem"]
        filme.video = request.form["video"]
        db.session.commit()
        return redirect(url_for("routes.home"))
    return render_template("editar.html", filme=filme)

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
