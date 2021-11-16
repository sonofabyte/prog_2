import sqlite3
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, g

DATABASE = 'notes.db'

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/notes")
def notes():
    return render_template('notes.html')        

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/media/<path:path>')
def send_media(path):
    return send_from_directory('static/media', path)

if __name__ == '__main__':
    app.run(debug=True)