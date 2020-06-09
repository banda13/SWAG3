""" NOTE: this file using relative pathing, so run this from the API folder! """
import os
import time
import json
import datetime
from flask import jsonify, request, send_file
from flask import Flask
from werkzeug.exceptions import abort

app = Flask(__name__,
            static_url_path='/static',
            static_folder='../results/',
            )

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/check', methods = ['GET'])
def check():
    return "<a href='{}'>Click me</a>".format("https://www.youtube.com/watch?v=QxnqkQEW4GU")


@app.route('/items', methods = ['GET'])
def items():
    response = []
    results = os.listdir("..\\results\\")
    for r in results:
        response.append({
            "name": r,
            "preview": "results\\" + r + "\\preview.png",
            "date": datetime.datetime.fromtimestamp(os.stat("..\\results\\" + r).st_mtime)
        })
    return jsonify(response)


@app.route("/objects", methods=['GET'])
def objects():
    name = request.args.get('name', None)
    if name is None:
        return abort(404)
    with open("..\\results\\" + name + "\\objects.txt", "r") as f:
        return jsonify([l.strip() for l in f.readlines()])


@app.route("/object_details", methods=['GET'])
def object_details():
    name = request.args.get('name', None)
    objectId = request.args.get("id", None)
    if name is None or objectId is None:
        return abort(404)
    with open("..\\results\\" + name + "\\objects\\" + str(objectId) + ".json") as f:
        return jsonify(json.load(f))


@app.route("/object_image", methods=['GET'])
def object_image():
    name = request.args.get('name', None)
    objectId = request.args.get("id", None)
    if name is None or objectId is None:
        return send_file("resources/error.jpg", mimetype='image/jpg')
    else:
        return send_file("..\\results\\" + name + "\\images\\" + str(objectId) + ".png", mimetype='image/png')


@app.route("/logs", methods=['GET'])
def logs():
    name = request.args.get('name', None)
    if name is None:
        return abort(404)
    else:
        with open("..\\results\\" + name + "\\debug.log", "r") as f:
            return jsonify([l.strip() for l in f.readlines()])



@app.route("/file", methods = ['GET'])
def file():
    filename = request.args.get('file', None)
    f, file_extension = os.path.splitext(filename)
    if not filename.startswith("results\\"):
        return send_file("resources/error.jpg", mimetype='image/jpg')
    else:
        return send_file("..\\" + filename,  mimetype='image/png')


if __name__ == '__main__':
    app.run('0.0.0.0', port=80)