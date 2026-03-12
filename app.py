from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///entregas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Entrega(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nf = db.Column(db.String(50))

    cliente = db.Column(db.String(200))

    endereco = db.Column(db.String(300))

    latitude = db.Column(db.Float)

    longitude = db.Column(db.Float)

    motorista = db.Column(db.String(100))

    status = db.Column(db.String(50))

    data = db.Column(db.String(20))


MOTORISTAS = [
    "José Marcos",
    "Paulo Cesar",
    "Silvio",
    "Deivid",
    "David"
]


def buscar_coordenadas(endereco):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": endereco,
        "format": "json"
    }

    r = requests.get(url, params=params)

    dados = r.json()

    if dados:

        lat = float(dados[0]["lat"])
        lon = float(dados[0]["lon"])

        return lat, lon

    return None, None


with app.app_context():
    db.create_all()


@app.route("/")
def dashboard():

    entregas = Entrega.query.all()

    total = len(entregas)

    pendente = 0
    saiu = 0
    entregue = 0

    ranking = {m: 0 for m in MOTORISTAS}

    for e in entregas:

        if e.status == "Pendente":
            pendente += 1

        elif e.status == "Saiu para entrega":
            saiu += 1

        elif e.status == "Entregue":
            entregue += 1
            ranking[e.motorista] += 1

    return render_template(
        "dashboard.html",
        entregas=entregas,
        total=total,
        pendente=pendente,
        saiu=saiu,
        entregue=entregue,
        ranking=ranking
    )


@app.route("/cadastro")
def cadastro():

    return render_template(
        "cadastro.html",
        motoristas=MOTORISTAS
    )


@app.route("/salvar", methods=["POST"])
def salvar():

    nf = request.form["nf"]

    cliente = request.form["cliente"]

    endereco = request.form["endereco"]

    motorista = request.form["motorista"]

    status = request.form["status"]

    data = datetime.now().strftime("%Y-%m-%d")

    lat, lon = buscar_coordenadas(endereco)

    nova = Entrega(
        nf=nf,
        cliente=cliente,
        endereco=endereco,
        latitude=lat,
        longitude=lon,
        motorista=motorista,
        status=status,
        data=data
    )

    db.session.add(nova)

    db.session.commit()

    return redirect(url_for("dashboard"))


@app.route("/status/<int:id>")
def atualizar_status(id):

    entrega = Entrega.query.get(id)

    if entrega.status == "Pendente":

        entrega.status = "Saiu para entrega"

    elif entrega.status == "Saiu para entrega":

        entrega.status = "Entregue"

    db.session.commit()

    return redirect(url_for("dashboard"))


@app.route("/rotas")
def rotas():

    entregas = Entrega.query.filter(Entrega.status != "Entregue").all()

    rotas = {}

    for e in entregas:

        rotas.setdefault(e.motorista, []).append(e)

    return render_template(
        "rotas.html",
        rotas=rotas
    )


@app.route("/motorista/<nome>")
def motorista(nome):

    entregas = Entrega.query.filter_by(motorista=nome).all()

    return render_template(
        "motorista.html",
        entregas=entregas,
        motorista=nome
    )


@app.route("/excluir/<int:id>")
def excluir(id):

    entrega = Entrega.query.get(id)

    db.session.delete(entrega)

    db.session.commit()

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)