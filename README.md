# Sticky Notes (App)

Eine kleine, einfache App für Notizen. 
Da ich immer meinen ganzen Schreibtisch voller Post-it Zettel habe, dachte ich mir ich programmiere eine Notes App. 
Eigentlich wollte ich noch ein Benutzer Login einfügen. Nach Absprache mit dem Dozenten, musste ich aber feststellen, dass es zu schwierig wird, ein "sicheres" Login zu erstellen. 

Die Notes App benutzt SQlite als Datenbank Anbindung. SQlite wurde ausgewählt, da man keinen externen Server braucht. Die Daten werden lokal in einer Datei gespeichert. 
Man muss sich auch nicht um die Sicherheit kümmern. Zudem muss auf einem anderen Rechner Nichts zusätzlich heruntergeladen/eingerichtet werden um die App zu starten. 

Ich hatte die Vision von einer "cleanen" Notes App. Dies konnte ich nur mit einem Pop-Up lösen, das sich öffnet. Das Pop-Up öffnet sich wenn man die Notes editieren oder neu erstellen möchte.
Bootstrap hat bereits ein solches Pop-Up. 
JavaScript füllt das Formular aus mit den bereits hinterlegten Daten sobald es geöffnet wird. Durch das drücken des "delete Buttons" wird durch JS die API in Phyton aufgerufen und die Notes aus der Datenbank gelöscht. 

## Verwendung

1. **Install Flask...**
1. type ```export FLASK_APP=app.py```, windows users use ```set FLASK_APP=app.py```
1. type ```flask run```

## Funktionen

- Schreiben von Textnotizen mit  Titeln
- Ändern von Notizen
- Notizen löschen

## Funktionen der App und deren Nutzen

def get_db --> Verbindung zu SQlite DB
def query_db --> Leseanfrage zu SQlite DB
def write_db --> Schreibanfrage zu SQlite DB
def default_route --> Umleitung auf Notes Seite
def notes --> Ganze Notiz Seite anzeigen
def modNote --> Neue Notiz erstellen, Bestehende Notiz bearbeiten, Für das bearbeiten abrufen mit Javascript
def delNote --> Nimmt die ID als POST-Parameter und löscht die Zeile in der DB, die der ID entspricht
def close_connection --> Schliesst SQlite bei exit

## Quellen und Inspirationen

- Python Flask Dokumentation <https://flask.palletsprojects.com/en/2.0.x/>
  - Wie Routes, Redirects, Datenbankverbindungen funktionieren
  - Wie man Flask dazu bringt, im Debug-Modus zu laufen
- Bootstrap-Dokumentation <https://getbootstrap.com>
- SQLite Sprachreferenz <https://www.sqlite.org/lang.html>
- SQLite mit Flask verwenden <https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/>

### Hintergrundbilder
Alle verwendeten Hintergrundbilder werden kostenlos von Unsplash.com zur Verfügung gestellt
- ```static/media/bg01.jpg```: Birger Strahl, Lüneburger Heide, Deutschland
- ```static/media/bg02.jpg```: Michael Benz, Elbow Falls, Kananaskis, Canada
