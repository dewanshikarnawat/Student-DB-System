from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc
from flask_cors import CORS
import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)
CONNECTION_STRING = os.getenv("SQL_CONNECTION_STRING")
# CONNECTION_STRING = (
#     "Driver={ODBC Driver 18 for SQL Server};"
#     "Server=tcp:studentdb-xebia1234.database.windows.net,1433;"
#     "Database=studentdb;"
#     "Uid=sqladmin;"
#     "Pwd=StudentDB@2026!;"
#     "Encrypt=yes;"
#     "TrustServerCertificate=no;"
#     "Connection Timeout=30;"
# )

def get_connection():
    return pyodbc.connect(CONNECTION_STRING)

# READ
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Students")

    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]

    result = [dict(zip(columns, row)) for row in rows]

    conn.close()
    return jsonify(result)

# CREATE
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Students (FirstName, LastName, Email, Course) VALUES (?, ?, ?, ?)",
        data['FirstName'],
        data['LastName'],
        data['Email'],
        data['Course']
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student added successfully"}), 201

# UPDATE
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Students SET FirstName=?, LastName=?, Email=?, Course=? WHERE StudentID=?",
        data['FirstName'],
        data['LastName'],
        data['Email'],
        data['Course'],
        student_id
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student updated successfully"})

# DELETE
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Students WHERE StudentID=?",
        student_id
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Student deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)