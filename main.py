from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/verificar', methods=['POST'])
def verificar_ots():
    if 'archivo' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo .ots'}), 400

    archivo = request.files['archivo']
    
    if archivo.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    if not archivo.filename.endswith('.ots'):
        return jsonify({'error': 'El archivo debe tener extensión .ots'}), 400

    ruta_archivo = os.path.join('/tmp', archivo.filename)
    archivo.save(ruta_archivo)

    try:
        resultado = subprocess.run(['ots', 'verify', ruta_archivo], capture_output=True, text=True)
        respuesta = {
            'salida': resultado.stdout,
            'error': resultado.stderr,
            'codigo_retorno': resultado.returncode
        }
        return jsonify(respuesta), 200 if resultado.returncode == 0 else 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
