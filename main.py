from flask import Flask, request, render_template
import hashlib
import opentimestamps

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    uploaded_file = request.files['file']
    file_bytes = uploaded_file.read()
    file_hash = hashlib.sha256(file_bytes).digest()
    try:
        result = opentimestamps.verify(file_hash)
        return render_template('result.html', result=result)
    except Exception as e:
        return render_template('result.html', result=f'Error: {e}')
