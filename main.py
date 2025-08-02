from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Autoris Verificador está activo.'

@app.route('/verify', methods=['GET'])
def verify():
    file_hash = request.args.get('file_hash')
    if not file_hash:
        return jsonify({'error': 'Falta el parámetro file_hash'}), 400

    # Crear archivo temporal .ots con el hash
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ots") as tmp_file:
        tmp_path = tmp_file.name
        try:
            tmp_file.write(bytes.fromhex(file_hash))
        except ValueError:
            return jsonify({'error': 'El hash no tiene un formato válido (debe estar en hexadecimal)'}), 400

    # Ejecutar la verificación
    try:
        result = subprocess.run(['ots', 'verify', tmp_path], capture_output=True, text=True)
        output = result.stdout + result.stderr
        if result.returncode == 0:
            status = 'válido'
        else:
            status = 'inválido o no verificable'
    except Exception as e:
        output = str(e)
        status = 'error'

    # Borrar archivo temporal
    os.remove(tmp_path)

    return jsonify({
        'hash': file_hash,
        'estado': status,
        'detalle': output
    })

if __name__ == '__main__':
    app.run(debug=True)
