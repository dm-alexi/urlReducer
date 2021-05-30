from flask import Flask, render_template, redirect, request, jsonify
from flask_pymongo import PyMongo
import random
from string import ascii_letters

URL_LENGTH = 7

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/shorturl"
mongo = PyMongo(app)
collection = mongo.db.shorts


def encode(url: str) -> str:
    line = ''.join(random.choice(ascii_letters) for _ in range(URL_LENGTH))
    record = collection.find_one({'short': line})
    while record:
        line = ''.join(random.choice(ascii_letters) for _ in range(URL_LENGTH))
        record = collection.find_one({'short': line})
    collection.insert_one({'short': line, 'url': url, 'counter': 0})
    return line


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v0', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        try:
            base = jsonify([x for x in collection.find({}, {'_id': False})])
        except Exception as ex:
            print(ex)
            return "Server error"
        return base
    else:
        url = request.json.get('url')
        if not url:
            return "Error: no URL provided"
        try:
            encoded = encode(url)
        except Exception as ex:
            print(ex)
            return "Server error"
        return request.url_root + encoded


@app.route('/<string:short_url>')
def handle_short(short_url):
    try:
        record = collection.find_one({'short': short_url})
        if record is None:
            return render_template('notfound.html', url=short_url)
        collection.update_one({'short': short_url}, {"$set": {'counter': record['counter'] + 1}})
    except Exception as ex:
        print(ex)
        return "Server error"
    return redirect(record['url'])


if __name__ == '__main__':
    app.run()
