from flask import Flask, request, jsonify, send_from_directory
import json
import os
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'automation_config.json')
TEST_CASE_PATH = os.path.join(os.path.dirname(__file__), 'test_case.json')

@app.route('/api/save-config', methods=['POST'])
def save_config():
    config = request.get_json()
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def serve_editor():
    return send_from_directory('.', 'config_editor.html')

@app.route('/api/get-test-case', methods=['GET'])
def get_test_case():
    try:
        with open(TEST_CASE_PATH, 'r', encoding='utf-8') as f:
            return jsonify({'success': True, 'content': f.read()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save-test-case', methods=['POST'])
def save_test_case():
    data = request.get_json()
    try:
        with open(TEST_CASE_PATH, 'w', encoding='utf-8') as f:
            f.write(data['content'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/run-main', methods=['POST'])
def run_main():
    try:
        result = subprocess.run(
            ['python', 'main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300  # 5 minutes
        )
        return jsonify({
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get-config', methods=['GET'])
def get_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return jsonify({'success': True, 'content': json.load(f)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)     