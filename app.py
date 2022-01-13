import sqlite3
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, g
import datetime

DATABASE = 'notes.db'

def get_db():
    """
    uses Flask to make connection to Sqlite DB

    code shamelessly stolen from Flask tutorial page
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    """
    uses Flask to make connection to Sqlite DB

    code shamelessly stolen from Flask tutorial page
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def write_db(query, args=(), one=False):
    """
    uses Flask to execute a write query (or query that doesn't return results) on Sqlite DB
    """
    cur = get_db().execute(query, args)
    get_db().commit()
    cur.close()

app = Flask(__name__)
app.secret_key = 'any random string'

@app.route("/")
def default_route():
    """
    this is the default route, just like the "index.html" file of a website. it however instantly redirects to the notes site.
    """
    return redirect(url_for('notes'))

@app.route("/notes", methods = ['GET', 'POST'])
def notes():
    """
    Route: /notes
    Methods: GET, POST
    """

    if request.method == 'GET':
        notes = query_db("select * from notes") # inspiration from flas SQLite documentation

        cards = []

        for note in notes:
            card = dict()
            card["ID"] = note[0]
            card["Title"] = note[1]
            card["Content"] = note[2]
            note_date = datetime.datetime.strptime(note[3], '%d/%m/%y %H:%M:%S') #parse datetime from SQL query as SQlite stores it as string, inspiration from stack overflow
            now_date = datetime.datetime.now()
            date_delta = now_date - note_date
            card["Modified"] = date_delta.days
            cards.append(card)

        return render_template('notes.html', cards = cards)
    if request.method == 'POST':
        return render_template('notes.html')

# inspiration: https://www.geeksforgeeks.org/retrieving-html-from-data-using-flask/
@app.route('/api/modNote', methods = ['POST'])
def modNote():
    """
    Route: /api/modNote
    Methods: POST
    Form Data:

    This endpoint serves three purposes:
        1. insert a new note into the database when the itemID field in the form is 0 (the SqliteDB generates a unique ID).
        2. edit an existing note in the database when the itemID field in the form is something else than 0 (Note in DB gets overwritten by new note).
        3. return a specific note in JSON format. the item_id field in POST body specifies the note. also a field named process with the value "get" has to be supplied.
    """
    if not ("process" in request.form):
        content = request.form.get("content", Text)
        title = request.form.get("title", Text)
        post_id = request.form.get("itemID", int)

        time_now_string = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')

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
    """
    Route: /api/delNote
    Methods: POST
    Form Data: item_id (the ID of the note in SQLite DB)

    Takes ID as POST parameter and deletes row in DB matching the ID
    """

    write_db('delete from notes where ID = ?', [request.form.get("item_id", int)])
    return dict() #return something, doesn't matter what

#Source: https://stackoverflow.com/questions/20646822/how-to-serve-static-files-in-flask
@app.route('/js/<path:path>') 
def send_js(path):
    """ Serves static JavaScript content """
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    """ Serves static CSS content """
    return send_from_directory('static/css', path)

@app.route('/media/<path:path>')
def send_media(path):
    """ Serves static Media content (images, or whatever is in that media folder) """
    return send_from_directory('static/media', path)

if __name__ == '__main__':
    app.run(debug=True)

# shut down SQlite on exit
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()