import datetime
from flask import jsonify
from flask import request
from backend import app
from backend.db_config import mysql
from backend.todo_entry import todo_entry


@app.route('/entries', methods=['GET'])
def get_all_entries():
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todo_entries")
        res = cursor.fetchall()
        data = [todo_entry(entry) for entry in res]
        return jsonify(data), 200
    except Exception as e:
        print(e)
        res = jsonify("An error occurred while updating the entry")
        return res, 500
    finally:
        cursor.close()
        conn.close()


@app.route('/entries/<todo_id>', methods=['GET'])
def get_entry_by_id(todo_id):
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todo_entries WHERE id=%s", [todo_id])
        res = cursor.fetchone()
        data = [todo_entry(res)]
        return jsonify(data), 200
    except Exception as e:
        print(e)
        res = jsonify("An error occurred while updating the entry")
        return res, 500
    finally:
        cursor.close()
        conn.close()


@app.route('/entries/<todo_id>', methods=['DELETE'])
def delete_entry_by_id(todo_id):
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todo_entries WHERE id=%s", [todo_id])
        conn.commit()
        res = jsonify("Deleted todo entry")
        return res, 200
    except Exception as e:
        print(e)
        res = jsonify("An error occurred while updating the entry")
        return res, 500
    finally:
        cursor.close()
        conn.close()


@app.route('/entries', methods=['POST'])
def create_entry():
    try:
        conn = mysql.connect
        cursor = conn.cursor()

        data = request.get_json()
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()
        content = data.get('content', '')
        title = data.get('title', '')
        completed = data.get('completed', 0)

        sql = "INSERT INTO todo_entries (created_at, updated_at, content, title, completed) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (created_at, updated_at,
                       content, title, completed))
        conn.commit()
        res = jsonify("User added successfully")
        return res, 200
    except Exception as e:
        print(e)
        res = jsonify("An error occurred while updating the entry")
        return res, 500
    finally:
        cursor.close()
        conn.close()


@app.route('/entries/<todo_id>', methods=['PATCH'])
def update_entry(todo_id):
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        data = request.get_json()
        updated_at = datetime.datetime.now()

        update_fields = []
        update_values = []

        if 'content' in data:
            update_fields.append("content=%s")
            update_values.append(data['content'])

        if 'title' in data:
            update_fields.append("title=%s")
            update_values.append(data['title'])

        if 'completed' in data:
            update_fields.append("completed=%s")
            update_values.append(data['completed'])

        if update_fields:
            update_fields.append("updated_at=%s")
            update_values.append(updated_at)
            update_values.append(todo_id)

        sql = f"UPDATE todo_entries SET {', '.join(update_fields)} WHERE id=%s"
        cursor.execute(sql, update_values)
        conn.commit()
        res = jsonify("User updated successfully")
        return res, 200

    except Exception as e:
        print(e)
        res = jsonify("An error occurred while updating the entry")
        return res, 500
    finally:
        cursor.close()
        conn.close()
