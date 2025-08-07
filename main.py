from flask import Flask, request, render_template
import subprocess
import os

app = Flask(__name__)

@app.route("/verificar_ots", methods=["GET", "POST"])
def verificar_ots():
    if request.method == "GET":
        return render_template("verificar_ots.html")

    original = request.files.get("original_file")
    ots = request.files.get("ots_file")

    if not original or not ots or original.filename == "" or ots.filename == "":
        return render_template("verificar_ots.html", resultado=True, archivo="Error", verificado=False, salida="Ambos archivos son requeridos.")

    original_path = f"/tmp/{original.filename}"
    ots_path = f"/tmp/{ots.filename}"

    try:
        original.save(original_path)
        ots.save(ots_path)

        result = subprocess.run(
            ["ots", "verify", ots_path, "--file", original_path],
            capture_output=True,
            text=True,
            timeout=10  # agregamos un timeout por seguridad
        )

        output = result.stdout + result.stderr
        verificado = "success" in output.lower()

        return render_template(
            "verificar_ots.html",
            resultado=True,
            archivo=ots.filename,
            verificado=verificado,
            salida=output
        )

    except subprocess.TimeoutExpired:
        return render_template("verificar_ots.html", resultado=True, archivo=ots.filename, verificado=False, salida="Tiempo de espera agotado al verificar el archivo.")
    except Exception as e:
        return render_template("verificar_ots.html", resultado=True, archivo=ots.filename, verificado=False, salida=f"Error inesperado: {e}")
    finally:
        for path in [original_path, ots_path]:
            if os.path.exists(path):
                os.remove(path)
