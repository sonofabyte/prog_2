import sqlite3
from typing import Text
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, g, session
import datetime

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


def write_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    get_db().commit()
    cur.close()

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route("/")
def hello_world():
    return redirect(url_for('notes'))

@app.route("/notes", methods = ['GET', 'POST'])
def notes():
    if request.method == 'GET':
        notes = query_db("select * from notes")

        cards = []

        for note in notes:
            card = dict()
            card["ID"] = note[0]
            card["Title"] = note[1]
            card["Content"] = note[2]
            note_date = datetime.datetime.strptime(note[3], '%d/%m/%y %H:%M:%S')
            now_date = datetime.datetime.now()
            date_delta = now_date - note_date
            card["Modified"] = date_delta.days
            cards.append(card)

        return render_template('notes.html', cards = cards)
    if request.method == 'POST':
        return render_template('notes.html')

@app.route('/api/modNote', methods = ['POST'])
def modNote():
    if not ("process" in request.form):
        content = request.form.get("content", Text)
        title = request.form.get("title", Text)
        post_id = request.form.get("itemID", int)

        time_now_string = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
        print(time_now_string)

        if int(request.form["itemID"]) == 0:
            # make new note in DB
            write_db('insert into notes (title, content, date) values (?, ?, ?)', [title, content, time_now_string])

        else:
            write_db('update notes set title = ?, content = ?, date = ? where ID = ?', [title, content, time_now_string, post_id])

        return redirect(url_for('notes'))

    elif request.form["process"] == "get":
        note = query_db('select * from notes where ID = ?', [request.form["item_id"]], one = True)
        resp = dict()
        resp["ID"] = note[0]
        resp["title"] = note[1]
        resp["content"] = note[2]
        return resp

@app.route('/api/delNote', methods = ['POST'])
def delNote():
    print("delNote ", request.form["item_id"])
    write_db('delete from notes where ID = ?', [request.form.get("item_id", int)])
    return dict() #return something, doesn't matter

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