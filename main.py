from flask import Flask, abort, request, Response
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)


def add_schema(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    return url


def sanitize_url(url):
    return url.replace('-', '.')


def get_absolute_url(base_url, relative_url):
    print(relative_url)
    return base_url + relative_url



def rewrite_links(base_url, html_content):
    # Rewrite relative links to absolute links
    soup = BeautifulSoup(html_content, 'html.parser')
    print(123454)
    # for tag in soup.find_all(['a', 'link', 'script', 'img']):
    #     if 'href' in tag.attrs:
    #         tag['href'] = get_absolute_url(base_url, tag['href'])
    #     if 'src' in tag.attrs:
    #         tag['src'] = get_absolute_url(base_url, tag['src'])
    #         # print(tag['src'])
    return str(soup)


@app.route('/<path:url>', methods=['GET'])
def get_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    }
    # print(url)
    if url is None:
        # Render a template or return a custom message
        return '<h1>Deployed!</h1><style>body { display: flex; align-items: center; justify-content: center; height: 100vh; }</style>'
    elif url:
        try:
            response = requests.get(sanitize_url(add_schema(url)), headers=headers)
            response.raise_for_status()
            # Rewrite links in the HTML content to point to the proxy server
            if 'image' in response.headers['content-type']:
                return Response(response.content, content_type=response.headers['content-type'])
            elif 'text/html' in response.headers['content-type']:
                base_url = str(url).split("/")[0]
                html_content = rewrite_links(base_url, response.content.decode('utf-8'))
                return Response(html_content, content_type=response.headers['content-type'])
            else:
                return response.content.decode('utf-8')
            # return Response(html_content)
        except requests.exceptions.RequestException as e:
            abort(400, description=e)
