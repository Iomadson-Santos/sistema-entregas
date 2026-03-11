import csv
from datetime import datetime

arquivo = "entregas.csv"

def cadastrar_entrega():
    cliente = input("Nome do cliente: ")
    bairro = input("Bairro: ")
    motorista = input("Motorista: ")
    status = input("Status da entrega: ")
    data = datetime.now().strftime("%d/%m/%Y")

    with open(arquivo, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([cliente, bairro, motorista, status, data])

    print("Entrega cadastrada com sucesso!")


def listar_entregas():
    try:
        with open(arquivo, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for linha in reader:

                if len(linha) < 5:
                    continue

                print(" | ".join(linha))

    except FileNotFoundError:
        print("Nenhuma entrega cadastrada.")


def buscar_motorista():
    nome = input("Digite o nome do motorista: ")

    try:
        with open(arquivo, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            encontrado = False

            for linha in reader:

                if len(linha) < 5:
                    continue

                if linha[2].lower() == nome.lower():
                    print(" | ".join(linha))
                    encontrado = True

            if not encontrado:
                print("Nenhuma entrega encontrada para esse motorista.")

    except FileNotFoundError:
        print("Arquivo de entregas não encontrado.")


def buscar_bairro():
    bairro = input("Digite o bairro: ")

    try:
        with open(arquivo, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            encontrado = False

            for linha in reader:

                if len(linha) < 5:
                    continue

                if linha[1].lower() == bairro.lower():
                    print(" | ".join(linha))
                    encontrado = True

            if not encontrado:
                print("Nenhuma entrega encontrada nesse bairro.")

    except FileNotFoundError:
        print("Arquivo de entregas não encontrado.")


def relatorio():
    try:
        with open(arquivo, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)

            total = 0
            pendente = 0
            saiu = 0
            entregue = 0
            motoristas = {}

            for linha in reader:

                if len(linha) < 5:
                    continue

                total += 1
                status = linha[3].lower()
                motorista = linha[2]

                if status == "pendente":
                    pendente += 1

                elif status == "saiu para entrega":
                    saiu += 1

                elif status == "entregue":
                    entregue += 1

                motoristas[motorista] = motoristas.get(motorista, 0) + 1

            print("\n===== DASHBOARD DE ENTREGAS =====")
            print("Total de entregas:", total)

            print("\nStatus das entregas:")
            print("Pendentes:", pendente)
            print("Saiu para entrega:", saiu)
            print("Entregues:", entregue)

            print("\nEntregas por motorista:")

            for motorista, quantidade in motoristas.items():
                print(motorista, "→", quantidade)

            if motoristas:
                top_motorista = max(motoristas, key=motoristas.get)
                print("\nMotorista com mais entregas:", top_motorista)

    except FileNotFoundError:
        print("Nenhuma entrega cadastrada.")


while True:

    print("\n===== SISTEMA DE ENTREGAS =====")
    print("1 - Cadastrar entrega")
    print("2 - Listar entregas")
    print("3 - Buscar por motorista")
    print("4 - Buscar por bairro")
    print("5 - Relatório")
    print("6 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_entrega()

    elif opcao == "2":
        listar_entregas()

    elif opcao == "3":
        buscar_motorista()

    elif opcao == "4":
        buscar_bairro()

    elif opcao == "5":
        relatorio()

    elif opcao == "6":
        print("Encerrando sistema...")
        break

    else:
        print("Opção inválida.")