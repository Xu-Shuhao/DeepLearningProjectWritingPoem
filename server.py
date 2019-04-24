# from __future__ import unicode_literals
import data, model
from config import *
from flask import Flask, json, render_template, request, jsonify
app = Flask(__name__)
trainData = data.POEMS(trainPoems)
ZuoShiJi = model.MODEL(trainData)

@app.route('/write', methods=['GET', 'POST'])
def write():

    data = json.loads(request.form.get('data'))
    head = data['value']
    poems = ZuoShiJi.testHead(head)

    # poems = '书生意气，挥斥方遒。\n指点江山，激扬文字。\n'
    return poems

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run()