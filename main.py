from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Microservicio de verificación de estampillas OTS en funcionamiento.'

@app.route('/verify')
def verify_hash():
    file_hash = request.args.get('file_hash')

    if not file_hash:
        return jsonify({'error': 'Parámetro file_hash requerido'}), 400

    try:
        result = subprocess.run(
            ['ots', 'verify', f'https://a.pool.opentimestamps.org/{file_hash}.ots'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            return jsonify({
                'hash': file_hash,
                'verificado': True,
                'mensaje': result.stdout
            })
        else:
            return jsonify({
                'hash': file_hash,
                'verificado': False,
                'error': result.stderr
            }), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
