from flask import jsonify
from backend import app
from backend.db_config import mysql


@app.route('/entries', methods=['GET'])
def get_all_entries():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo_entries")
    response = cursor.fetchall()
    cursor.close()
    return jsonify(response)


@app.route('/entries/<id>', methods=['GET'])
def get_entry_by_id(id):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo_entries WHERE id=%s", [id])
    response = cursor.fetchone()
    cursor.close()
    return jsonify(response)
