from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Autoris Verificador está en línea."

@app.route("/verify", methods=["GET"])
def verify():
    file_hash = request.args.get("file_hash")

    if not file_hash:
        return jsonify({"error": "Falta el parámetro 'file_hash'."}), 400

    try:
        result = subprocess.run(
            ["ots", "verify", file_hash],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return jsonify({
            "success": True,
            "output": result.stdout.strip()
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "success": False,
            "error": e.stderr.strip()
        }), 500
