from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Servicio de verificación en línea"

@app.route("/verify")
def verify():
    file_hash = request.args.get("file_hash")
    if not file_hash:
        return "No se recibió ningún hash", 400
    return f"Recibido el hash: {file_hash}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
