
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('concessioni_edilizie.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    comune = request.args.get('comune')
    categoria = request.args.get('categoria')
    destinazione = request.args.get('destinazione')
    data_inizio = request.args.get('data_inizio')
    data_fine = request.args.get('data_fine')

    query = "SELECT * FROM concessioni_edilizie WHERE 1=1"
    params = []

    if comune:
        query += " AND comune LIKE ?"
        params.append(f"%{comune}%")
    if categoria:
        query += " AND categoria_edificio LIKE ?"
        params.append(f"%{categoria}%")
    if destinazione:
        query += " AND destinazione_uso LIKE ?"
        params.append(f"%{destinazione}%")
    if data_inizio:
        query += " AND data_concessione >= ?"
        params.append(data_inizio)
    if data_fine:
        query += " AND data_concessione <= ?"
        params.append(data_fine)

    conn = get_db_connection()
    results = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(row) for row in results])

if __name__ == '__main__':
    app.run(debug=True)
    port = int(os.environ.get("PORT", 10000))  # Usa la porta fornita da Render
    app.run(host='0.0.0.0', port=port)

import sqlite3

