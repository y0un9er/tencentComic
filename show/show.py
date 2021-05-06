# coding=utf-8

import base64
import json
import os

import requests
from flask import Flask
from flask import request, render_template, send_file

app = Flask(__name__)


@app.route('/')
def index():
    allComic = os.listdir('../comic')
    return render_template('index.html', allComic=allComic)


@app.route('/comic/<title>/<int:page>')
def comic(title, page=1):
    with open(f'../comic/{title}/{title}.json') as f:
        json_data = json.load(f)

        chapter = list(list(json_data.values())[0].items())[page - 1]
        chapter_name = chapter[0]

        imgs = chapter[1].values()

        return render_template('comic.html', title=title, chapter_name=chapter_name, imgs=imgs, page=page)


@app.route('/getImg', methods=['POST'])
def getImg():
    try:
        url = request.form['url']

        response = requests.get(url)

        return str(base64.b64encode(response.content), encoding='utf-8')
    except:
        return '#'


@app.route('/cover/<title>')
def cover(title):
    image = open(f'../comic/{title}/cover.png', 'rb')
    return send_file(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
