from flask import Flask, request, redirect, jsonify
import string
import random

app = Flask(__name__)

# In-memory database
url_mapping = {}
BASE_URL = "http://localhost:5000/"
SHORT_ID_LENGTH = 6

def generate_short_id(length=SHORT_ID_LENGTH):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    short_id = generate_short_id()
    while short_id in url_mapping:
        short_id = generate_short_id()

    url_mapping[short_id] = original_url
    short_url = BASE_URL + short_id

    return jsonify({'short_url': short_url}), 201

@app.route('/<short_id>')
def redirect_to_original(short_id):
    original_url = url_mapping.get(short_id)
    if original_url:
        return redirect(original_url)
    return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
