from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_db():
    return mysql.connector.connect(
        host="database_ip_address",
        user="notes_user",
        password="password",
        database="notes_db"
    )

@app.route("/notes", methods=["GET"])
def get_notes():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()

    result = [{"id": r[0], "content": r[1]} for r in rows]

    cursor.close()
    db.close()

    return jsonify(result)

@app.route("/notes", methods=["POST"])
def add_note():
    try:
        data = request.get_json()

        db = get_db()
        cursor = db.cursor()

        # ✅ FIX: use %s for MySQL
        cursor.execute("INSERT INTO notes (content) VALUES (%s)", (data["content"],))
        db.commit()

        cursor.close()
        db.close()

        return jsonify({"message": "Note added"}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    try:
        db = get_db()
        cursor = db.cursor()

        # ✅ FIX: use %s
        cursor.execute("DELETE FROM notes WHERE id=%s", (id,))
        db.commit()

        cursor.close()
        db.close()

        return jsonify({"message": "Deleted"}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
