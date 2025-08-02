from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

@app.route("/verificar_ots", methods=["GET", "POST"])
def verificar_ots():
    if request.method == "GET":
        return render_template("verificar_ots.html")

    if "ots_file" not in request.files:
        return jsonify({"error": "No se envió ningún archivo .ots"}), 400

    file = request.files["ots_file"]

    if file.filename == "":
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)

    try:
        result = subprocess.run(["ots", "verify", temp_path], capture_output=True, text=True)
        output = result.stdout + result.stderr
        verificado = "success" in output.lower()
        return jsonify({
            "archivo": file.filename,
            "verificado": verificado,
            "salida": output
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# Bloque para correr la app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
