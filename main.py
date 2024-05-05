from flask import Flask, jsonify, abort
import requests

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
}

def add_schema(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    return url

# Define a route for the GET request
@app.route('/url/<path:url>', methods=['GET'])
def get_url(url):
    try:
        print(add_schema(url))
        request = requests.get(add_schema(url), headers=headers)
        request.raise_for_status()
        return request.content.decode('utf-8')
    except requests.exceptions.RequestException as s:
        abort(400, description=s)

if __name__ == '__main__':
    app.run(debug=True)