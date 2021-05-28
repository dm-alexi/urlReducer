from flask import Flask, render_template, redirect, request
import random
from string import ascii_letters

URL_LENGTH = 7

app = Flask(__name__)
base = {}


def encode(url: str) -> str:
    line = ''.join(random.choice(ascii_letters) for _ in range(URL_LENGTH))
    while line in base:
        line = ''.join(random.choice(ascii_letters) for _ in range(URL_LENGTH))
    base[line] = [url, 0]
    return line


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        url = request.json.get('url')
        if url is None:
            return "No url provided"
        return request.url_root + encode(url)


@app.route('/<string:short_url>')
def handle_short(short_url):
    if short_url in base:
        base[short_url][1] += 1
        return redirect(base[short_url][0])
    return render_template('notfound.html', url=short_url)


if __name__ == '__main__':
    app.run()
