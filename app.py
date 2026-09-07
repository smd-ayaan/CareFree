"""
app.py — Flask bridge between carepass.html (frontend) and the Python backend.

Run with:
    python app.py

Then open in your browser:
    http://127.0.0.1:5000
"""
import os
from flask import Flask, jsonify, send_from_directory

from database import init_db
from face_service import scan_face

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
init_db()


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "carepass.html")


@app.route("/api/scan", methods=["POST"])
def api_scan():
    result = scan_face()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)