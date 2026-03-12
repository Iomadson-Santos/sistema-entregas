from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)

ARQUIVO = "entregas.csv"

MOTORISTAS = [
    "José Marcos",
    "Paulo Cesar",
    "Silvio",
    "Deivid",
    "David"
]


def ler_entregas():

    entregas = []

    if not os.path.exists(ARQUIVO):
        return entregas

    with open(ARQUIVO, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for i, linha in enumerate(reader):

            if len(linha) < 6:
                continue

            entregas.append({
                "id": i,
                "nf": linha[0],
                "cliente": linha[1],
                "endereco": linha[2],
                "motorista": linha[3],
                "status": linha[4],
                "data": linha[5]
            })

    return entregas


def salvar_csv(linhas):

    with open(ARQUIVO, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)
        writer.writerows(linhas)


@app.route("/")
def dashboard():

    entregas = ler_entregas()

    total = len(entregas)
    pendente = 0
    saiu = 0
    entregue = 0

    ranking = {m: 0 for m in MOTORISTAS}

    for e in entregas:

        status = e["status"]

        if status == "Pendente":
            pendente += 1

        elif status == "Saiu para entrega":
            saiu += 1

        elif status == "Entregue":
            entregue += 1
            ranking[e["motorista"]] += 1

    ranking = dict(sorted(ranking.items(), key=lambda x: x[1], reverse=True))

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

    nf = request.form.get("nf")
    cliente = request.form.get("cliente")
    endereco = request.form.get("endereco")
    motorista = request.form.get("motorista")
    status = request.form.get("status")

    data = datetime.now().strftime("%d/%m/%Y")

    with open(ARQUIVO, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            nf,
            cliente,
            endereco,
            motorista,
            status,
            data
        ])

    return redirect(url_for("dashboard"))


@app.route("/status/<int:id>")
def atualizar_status(id):

    linhas = []

    with open(ARQUIVO, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for i, linha in enumerate(reader):

            if i == id:

                if linha[4] == "Pendente":
                    linha[4] = "Saiu para entrega"

                elif linha[4] == "Saiu para entrega":
                    linha[4] = "Entregue"

            linhas.append(linha)

    salvar_csv(linhas)

    return redirect(url_for("dashboard"))


@app.route("/excluir/<int:id>")
def excluir(id):

    linhas = []

    with open(ARQUIVO, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for i, linha in enumerate(reader):

            if i != id:
                linhas.append(linha)

    salvar_csv(linhas)

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)