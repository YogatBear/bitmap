from flask import Flask, render_template, request, jsonify
import numpy as np
import cv2
import random
import sys
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/grid', methods = ['POST', 'GET'])
def grid():
    form_data = request.form
    rows = int(form_data['rows'])
    columns = int(form_data['columns'])
    output = []

    if request.form['action'] == 'RANDOMIZE':
        for i in range(rows*columns):
            output.append(random.randint(0, 1))

        return render_template('grid.html', rows=rows, columns=columns, output=output)

    elif request.form['action'] == 'DRAW':
        for i in range (rows*columns):
            output.append(0)

        return render_template('draw.html', rows=rows, columns=columns, output=output)

@app.route('/plot', methods = ['POST', 'GET'])
def plot():
    if request.method == 'POST':
        form_data = request.form
        rows = int(form_data['rows'])
        columns = int(form_data['columns'])
        if 'output' in request.form:
            output = form_data['output'][1:-1].split(', ')
            print(output)
        else:
            output = form_data['output2'][2:-2].split('","')
            print(output)
        mat = []
        while output != []:
            mat.append(output[:columns])
            output = output[columns:]
        array = np.array(mat, dtype= np.uint8)
        cv_array = array.astype(np.uint8)
        print(cv_array)
        labels, labled_array = cv2.connectedComponents(cv_array)
        print(labled_array)
        for r in (labled_array):
            for i in r:
                output.append(i)
        colors = ['white']
        for i in range(labels-1):
            colors.append("#{:06x}".format(random.randint(0, 0xFFFFFF)))
                               
        return render_template('plot.html', output=output, colors=colors, columns=columns, rows=rows, labels=labels)

if __name__ == '__main__':
    app.debug = True
    app.run()