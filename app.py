from flask import Flask, render_template, request, redirect
import csv
import pandas as pd
from datetime import datetime

app = Flask(__name__)

arquivo = "entregas.csv"

motoristas = [
    "José Marcos",
    "Paulo Cesar",
    "Silvio",
    "Deivid",
    "David"
]


def ler_entregas():

    entregas = []

    try:
        with open(arquivo, "r", encoding="utf-8") as file:

            reader = csv.reader(file)

            for i, linha in enumerate(reader):

                entregas.append({
                    "id": i,
                    "nf": linha[0],
                    "cliente": linha[1],
                    "endereco": linha[2],
                    "motorista": linha[3],
                    "status": linha[4],
                    "data": linha[5]
                })

    except:
        pass

    return entregas


@app.route("/")
def dashboard():

    entregas = ler_entregas()

    total = len(entregas)
    pendente = 0
    saiu = 0
    entregue = 0

    desempenho = {}

    for m in motoristas:
        desempenho[m] = 0

    for e in entregas:

        if e["status"] == "Pendente":
            pendente += 1

        elif e["status"] == "Saiu para entrega":
            saiu += 1

        elif e["status"] == "Entregue":
            entregue += 1
            desempenho[e["motorista"]] += 1

    return render_template(
        "dashboard.html",
        entregas=entregas,
        total=total,
        pendente=pendente,
        saiu=saiu,
        entregue=entregue,
        desempenho=desempenho
    )


@app.route("/cadastro")
def cadastro():

    return render_template(
        "cadastro.html",
        motoristas=motoristas
    )


@app.route("/salvar", methods=["POST"])
def salvar():

    nf = request.form["nf"]
    cliente = request.form["cliente"]
    endereco = request.form["endereco"]
    motorista = request.form["motorista"]
    status = request.form["status"]

    data = datetime.now().strftime("%d/%m/%Y")

    with open(arquivo, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)
        writer.writerow([nf, cliente, endereco, motorista, status, data])

    return redirect("/")


@app.route("/importar", methods=["POST"])
def importar():

    file = request.files["arquivo"]

    df = pd.read_excel(file)

    with open(arquivo, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        for _, row in df.iterrows():

            writer.writerow([
                row["NF"],
                row["Cliente"],
                row["Endereco"],
                row["Motorista"],
                row["Status"],
                datetime.now().strftime("%d/%m/%Y")
            ])

    return redirect("/")


@app.route("/status/<int:id>")
def atualizar_status(id):

    linhas = []

    with open(arquivo, "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        for i, linha in enumerate(reader):

            if i == id:

                if linha[4] == "Pendente":
                    linha[4] = "Saiu para entrega"

                elif linha[4] == "Saiu para entrega":
                    linha[4] = "Entregue"

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


@app.route("/rotas")
def rotas():

    entregas = ler_entregas()

    rotas = {}

    for m in motoristas:
        rotas[m] = []

    for e in entregas:

        if e["status"] != "Entregue":
            rotas[e["motorista"]].append(e)

    return render_template(
        "rotas.html",
        rotas=rotas
    )


if __name__ == "__main__":
    app.run(debug=True)