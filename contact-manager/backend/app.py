from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

#-----------------------------------sql-------------------------------------
import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

#-------------------------------rotas----------------------------------

#get_contatc (buscar os contactos)
@app.route("/contacts", methods=["GET"])
def get_contacts():
    conn = sqlite3.connect("database.db")#conectar a base de dados
    cur = conn.cursor()#criar cursor "trabalhador"
    cur.execute("SELECT * FROM contacts")#seleciona todos os contactos e todos os parametros

    row = cur.fetchall()
    conn.close()
    
    result = []
    for i in row:
        result.append({"id":i[0],"name":i[1],"email":i[2],"phone":i[3]})

    return jsonify(result)

#post_contact (criar novo contacto)
@app.route("/contacts", methods=["POST"]) #POST
def post_contacts():
    data = request.get_json()
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)",
                (data.get("name"), data.get("email"), data.get("phone")))
    conn.commit()# ← Confirma e grava na database
    conn.close()
    return jsonify({"message": "Contact added successfully"}), 201

#Update_contacts(dar update nos contactos, mudar alguma coisa em um especifico)
@app.route("/contacts/<int:contact_id>", methods=["PUT"]) #update
def put_contacts(contact_id):
    data = request.get_json()

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("UPDATE contacts SET name = ?, email = ?, phone = ? WHERE id = ?",
                (data.get("name"), data.get("email"), data.get("phone"), contact_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Contact updated successfully"}), 200

#Delete_contact (apagar contacto)
@app.route("/contacts/<int:contact_id>", methods=["DELETE"]) #Delete
def delete_contact(contact_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Contact was fully deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)