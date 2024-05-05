from flask import Flask, jsonify, abort, request
import requests

app = Flask(__name__)

def add_schema(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    return url



@app.route('/', methods=['GET'])
def get_url():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    }

    url_param = request.args.get('url')

    if url_param is None:
        # Render a template or return a custom message
        return '<h1>Deployed!</h1><style>body { display: flex; align-items: center; justify-content: center; height: 100vh; }</style>'
    elif url_param:
        try:
            print(add_schema(url))
            request = requests.get(add_schema(url), headers=headers)
            request.raise_for_status()
            return request.content.decode('utf-8')
        except requests.exceptions.RequestException as s:
            abort(400, description=s)