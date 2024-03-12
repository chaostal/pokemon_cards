from flask import Flask
from flask import render_template, request, jsonify, g
from werkzeug.utils import secure_filename
import csv
import sqlite3
import os

app = Flask(__name__)

# set some facts
DATABASE = 'pokemonkarten.db'
UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = {'csv', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# some simple helper functions
# return dicts from a table
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# get the db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db

# close the db on app teardown
@app.teardown_appcontext
def close_connection(exeption):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# initialize the db if starting for the first time
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# query the db
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# start routes
@app.route('/', methods=['GET','POST'])
def index():
    cards = query_db('SELECT * FROM pokemonkarten')
    if request.method == 'POST':
        results = []
        for card in cards:
            if request.form['name'] != '':
                if request.form['name'] in card['Name']:
                    results.append(card)
            if request.form['typ'] != '':
                if request.form['typ'] in card['Typ']:
                    results.append(card)
            if request.form['serie'] != 'none':
                if request.form['serie'] in card['Serie']:
                    results.append(card)
            if request.form['seltenheit'] != 'none':
                if request.form['seltenheit'] in card['Seltenheit']:
                    results.append(card)

        if results:
            return render_template('suche.html', results = results)
        else:
            return render_template('suche.html', results = '')
    else:
        return render_template('index.html', cards = cards)

@app.route('/karte/neu', methods=['GET','POST'])
def karte_neu():
    if request.method == 'POST':
        cur = get_db().cursor()

        Name = request.form['name']
        Typ = request.form['typ']
        Serie = request.form['serie']
        Entwicklung = request.form['entwicklung']
        Kp = request.form['kp']
        Seltenheit = request.form['seltenheit']
        Holo = request.form['holo']
        Special = request.form['special']
        Schwaeche = request.form['schwaeche']
        Resistenz = request.form['resistenz']
        Anzahl = request.form['anzahl']
        Sprache = request.form['sprache']
        Decks = request.form['decks']

        cur.execute('INSERT INTO pokemonkarten(Name,Typ,Serie,Entwicklung,Kp,Seltenheit,Holo,Special,Schwaeche,Resistenz,Anzahl,Sprache,Decks) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',(Name,Typ,Serie,Entwicklung,Kp,Seltenheit,Holo,Special,Schwaeche,Resistenz,Anzahl,Sprache,Decks))
        get_db().commit()
        get_db().close()
        return request.form
    else:
        return render_template('karte.html')

@app.route('/karten/importieren', methods=['GET','POST'])
def karten_import():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Die Datei fehlt..."
        file = request.files['file']
        if file.filename == '':
            return "Die Datei fehlt..."

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('download_file', name=filename))

        raw_cards = open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cards = csv.DictReader(raw_cards)
        cur = get_db().cursor()
        for card in cards:

            Name = card['Name']
            Typ = card['Typ']
            Staerke = card['Stärke']
            Abwehr = card['Abwehr']
            Farbe = card['Farbe']
            Kosten = card['Manakosten']
            Seltenheit = card['Seltenheit']
            Holo = card['Holo']
            Serie = card['Serie']
            Sprache = card['Sprache']
            Anzahl = card['Anzahl']
            Decks = card['Decks']

            cur.execute('INSERT INTO magickarten(Name,Typ,Staerke,Farbe,Kosten,Abwehr,Seltenheit,Holo,Serie,Sprache,Anzahl,Decks) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',(Name,Typ,Staerke,Farbe,Kosten,Abwehr,Seltenheit,Holo,Serie,Sprache,Anzahl,Decks))
            get_db().commit()

        cur.close()

        return "\o/ Alle Karten importiert"
    else:
        return render_template('csv_import.html')
