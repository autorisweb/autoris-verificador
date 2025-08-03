from flask import Flask, request, render_template
import subprocess
import os

app = Flask(__name__)

@app.route("/verificar_ots", methods=["GET", "POST"])
def verificar_ots():
    if request.method == "GET":
        return render_template("verificar_ots.html")

    if "original_file" not in request.files or "ots_file" not in request.files:
        return render_template("verificar_ots.html", resultado=True, archivo="Error", verificado=False, salida="Ambos archivos son requeridos.")

    original = request.files["original_file"]
    ots = request.files["ots_file"]

    if original.filename == "" or ots.filename == "":
        return render_template("verificar_ots.html", resultado=True, archivo="Error", verificado=False, salida="Archivos inválidos.")

    original_path = f"/tmp/{original.filename}"
    ots_path = f"/tmp/{ots.filename}"

    original.save(original_path)
    ots.save(ots_path)

    try:
        result = subprocess.run(
            ["ots", "verify", ots_path, "--file", original_path],
            capture_output=True,
            text=True
        )
        output = result.stdout + result.stderr
        verificado = "success" in output.lower()
        return render_template("verificar_ots.html", resultado=True, archivo=ots.filename, verificado=verificado, salida=output)
    except Exception as e:
        return render_template("verificar_ots.html", resultado=True, archivo=ots.filename, verificado=False, salida=str(e))
    finally:
        for path in [original_path, ots_path]:
            if os.path.exists(path):
                os.remove(path)
