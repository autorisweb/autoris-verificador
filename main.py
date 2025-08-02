from flask import Flask, request, jsonify
import subprocess
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def home():
    return 'Microservicio de Verificación con OpenTimestamps activo ✅'

@app.route('/verify')
def verificar_hash():
    file_hash = request.args.get('file_hash')
    if not file_hash:
        return jsonify({'error': 'Falta el parámetro file_hash'}), 400

    ots_url = f'https://a.pool.opentimestamps.org/{file_hash}.ots'

    try:
        result = subprocess.run(
            ['ots', 'verify', ots_url],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return jsonify({
                'hash': file_hash,
                'verificado': True,
                'resultado': result.stdout
            })
        else:
            return jsonify({
                'hash': file_hash,
                'verificado': False,
                'error': result.stderr
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verificar_ots', methods=['POST'])
def verificar_ots_desde_archivo():
    if 'archivo' not in request.files:
        return jsonify({'error': 'No se subió ningún archivo'}), 400

    archivo = request.files['archivo']

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        ruta_temp = tmp.name
        archivo.save(ruta_temp)

    try:
        resultado = subprocess.run(
            ['ots', 'verify', ruta_temp],
            capture_output=True,
            text=True
        )

        os.remove(ruta_temp)

        if resultado.returncode == 0:
            return jsonify({
                'verificado': True,
                'resultado': resultado.stdout
            })
        else:
            return jsonify({
                'verificado': False,
                'error': resultado.stderr
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
