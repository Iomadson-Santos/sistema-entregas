import csv
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, redirect, send_file

app = Flask(__name__)

arquivo = "entregas.csv"


def ler_entregas():

    entregas = []

    try:
        with open(arquivo, "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            for i, linha in enumerate(reader):

                if len(linha) < 5:
                    continue

                entregas.append({
                    "id": i,
                    "cliente": linha[0],
                    "bairro": linha[1],
                    "motorista": linha[2],
                    "status": linha[3],
                    "data": linha[4]
                })

    except FileNotFoundError:
        pass

    return entregas


def ler_motoristas():

    motoristas = []

    try:

        with open("motoristas.csv", "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            for linha in reader:

                motoristas.append({
                    "nome": linha[0],
                    "veiculo": linha[1]
                })

    except FileNotFoundError:
        pass

    return motoristas


@app.route("/")
def dashboard():

    entregas = ler_entregas()

    total = len(entregas)

    pendente = sum(1 for e in entregas if e["status"] == "Pendente")
    saiu = sum(1 for e in entregas if e["status"] == "Saiu para entrega")
    entregue = sum(1 for e in entregas if e["status"] == "Entregue")

    motoristas = {}

    for e in entregas:

        nome = e["motorista"]

        motoristas[nome] = motoristas.get(nome, 0) + 1

    nomes = list(motoristas.keys())
    quantidades = list(motoristas.values())

    return render_template(
        "dashboard.html",
        entregas=entregas,
        total=total,
        pendente=pendente,
        saiu=saiu,
        entregue=entregue,
        nomes=nomes,
        quantidades=quantidades
    )


@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


@app.route("/salvar", methods=["POST"])
def salvar():

    cliente = request.form["cliente"]
    bairro = request.form["bairro"]
    motorista = request.form["motorista"]
    status = request.form["status"]

    data = datetime.now().strftime("%d/%m/%Y")

    with open(arquivo, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([cliente, bairro, motorista, status, data])

    return redirect("/")


@app.route("/editar/<int:id>")
def editar(id):

    with open(arquivo, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        linhas = list(reader)

    entrega = linhas[id]

    return render_template("editar.html", entrega=entrega, id=id)


@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):

    linhas = []

    with open(arquivo, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for i, linha in enumerate(reader):

            if i == id:

                cliente = request.form["cliente"]
                bairro = request.form["bairro"]
                motorista = request.form["motorista"]
                status = request.form["status"]

                data = linha[4]

                linha = [cliente, bairro, motorista, status, data]

            linhas.append(linha)

    with open(arquivo, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerows(linhas)

    return redirect("/")


@app.route("/status/<int:id>")
def atualizar_status(id):

    linhas = []

    with open(arquivo, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for i, linha in enumerate(reader):

            if i == id:

                if linha[3] == "Pendente":
                    linha[3] = "Saiu para entrega"

                elif linha[3] == "Saiu para entrega":
                    linha[3] = "Entregue"

            linhas.append(linha)

    with open(arquivo, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerows(linhas)

    return redirect("/")


@app.route("/excluir/<int:id>")
def excluir(id):

    linhas = []

    with open(arquivo, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for i, linha in enumerate(reader):

            if i != id:
                linhas.append(linha)

    with open(arquivo, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerows(linhas)

    return redirect("/")


@app.route("/motorista")
def tela_motorista():

    entregas = ler_entregas()

    entregas_pendentes = [e for e in entregas if e["status"] != "Entregue"]

    return render_template("motorista.html", entregas=entregas_pendentes)


@app.route("/rotas")
def rotas():

    entregas = ler_entregas()

    rotas = {}

    for e in entregas:

        bairro = e["bairro"]

        rotas[bairro] = rotas.get(bairro, 0) + 1

    return render_template("rotas.html", rotas=rotas)


@app.route("/exportar")
def exportar():

    df = pd.read_csv("entregas.csv")

    df.columns = [
        "Cliente",
        "Bairro",
        "Motorista",
        "Status",
        "Data"
    ]

    arquivo_excel = "relatorio_entregas.xlsx"

    df.to_excel(arquivo_excel, index=False)

    return send_file(arquivo_excel, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)