from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# -----------------------------
# BANCO DE DADOS
# -----------------------------
def conectar_banco():
    return sqlite3.connect("emails.db")

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

criar_tabela()

def criar_tabela_envios():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            data_envio TEXT
        )
    """)
    conn.commit()
    conn.close()

criar_tabela_envios()


# -----------------------------
# ROTAS
# -----------------------------

@app.route("/contacts", methods=["GET"])
def listar_contatos():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contatos")
    contatos = cursor.fetchall()
    conn.close()

    lista = []
    for c in contatos:
        lista.append({
            "id": c[0],
            "nome": c[1],
            "email": c[2]
        })

    return jsonify(lista)


@app.route("/contacts", methods=["POST"])
def adicionar_contato():
    dados = request.json
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contatos (nome, email) VALUES (?, ?)",
        (dados["nome"], dados["email"])
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@app.route("/contacts/<int:id>", methods=["DELETE"])
def remover_contato(id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contatos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "removido"})

from datetime import datetime

@app.route("/send-campaign", methods=["POST"])
def enviar_campanha():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM contatos")
    contatos = cursor.fetchall()

    for contato in contatos:
        cursor.execute(
            "INSERT INTO envios (email, data_envio) VALUES (?, ?)",
            (contato[0], datetime.now().strftime("%d/%m/%Y %H:%M"))
        )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "campanha_enviada",
        "total": len(contatos)
    })
@app.route("/reports", methods=["GET"])
def listar_relatorios():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT email, data_envio FROM envios")
    dados = cursor.fetchall()
    conn.close()

    relatorios = []
    for item in dados:
        relatorios.append({
            "email": item[0],
            "data": item[1]
        })

    return jsonify(relatorios)
import csv

@app.route("/reports/csv", methods=["GET"])
def exportar_csv():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT email, data_envio FROM envios")
    dados = cursor.fetchall()
    conn.close()

    with open("relatorio_envios.csv", "w", newline="") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["Email", "Data de Envio"])
        writer.writerows(dados)

    return jsonify({"status": "csv_gerado"})

if __name__ == "__main__":
    app.run(debug=True)
