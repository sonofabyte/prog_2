import sqlite3
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, g, session

DATABASE = 'notes.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route("/")
def hello_world():
    return redirect(url_for('notes'))

@app.route("/notes", methods = ['GET', 'POST'])
def notes():
    if request.method == 'GET':
        notes = query_db("select * from notes")
        print(notes)
        return render_template('notes.html')
    if request.method == 'POST':
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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()