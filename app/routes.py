from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    filmes = [
        {
            "id": 1,
            "titulo": "O Poderoso Chefão",
            "imagem": "images/filme1.jpg",
            "descricao": "Um clássico da máfia que marcou gerações.",
            "video": "videos/filme1.mp4"
        },
        {
            "id": 2,
            "titulo": "Interestelar",
            "imagem": "images/filme2.jpg",
            "descricao": "Uma jornada épica pelo espaço e tempo.",
            "video": "videos/filme2.mp4"
        },
        {
            "id": 3,
            "titulo": "Matrix",
            "imagem": "images/filme3.jpg",
            "descricao": "A realidade é uma ilusão?",
            "video": "videos/filme3.mp4"
        }
    ]
    return render_template("index.html", filmes=filmes)

@app.route("/assistir/<int:filme_id>")
def assistir(filme_id):
    filmes = {
        1: {
            "titulo": "O Poderoso Chefão",
            "video": "videos/filme1.mp4"
        },
        2: {
            "titulo": "Interestelar",
            "video": "videos/filme2.mp4"
        },
        3: {
            "titulo": "Matrix",
            "video": "videos/filme3.mp4"
        }
    }
    filme = filmes.get(filme_id)
    if not filme:
        return "Filme não encontrado", 404
    return render_template("assistir.html", filme=filme)
