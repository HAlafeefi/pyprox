from flask import Flask, abort, request
import requests

app = Flask(__name__)

def add_schema(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    return url

def sanitize_url(url):
    return url.replace('-', '.')

@app.route('/<path:url>', methods=['GET'])
def get_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    }
    print(url)
    if url is None:
        # Render a template or return a custom message
        return '<h1>Deployed!</h1><style>body { display: flex; align-items: center; justify-content: center; height: 100vh; }</style>'
    elif url:
        try:
            request1 = requests.get(sanitize_url(add_schema(url)), headers=headers)
            request1.raise_for_status()
            return request1.content.decode('utf-8')
        except requests.exceptions.RequestException as s:
            abort(400, description=s)