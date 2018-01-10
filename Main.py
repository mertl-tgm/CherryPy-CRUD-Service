import os.path
import sqlite3
from time import sleep

import cherrypy

DB_STRING = "datenbank.db"


class CRUD(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')


@cherrypy.expose
class CRUDWebService(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, param, input):
        print("TEST submit button :" + input)
        if param == "read":
            with sqlite3.connect(DB_STRING) as c:
                r = c.execute("SELECT * FROM benutzer")
                response = "<table width='100%' class='table table-striped table-bordered'" \
                           "cellspacing='0'><tr><td>Nr</td><td>Vorname</td><td>Nachname</td>" \
                           "<td>Username</td></tr>"
                while True:
                    row = r.fetchone()
                    if row is None:
                        break
                    response += "<tr><td>" + str(row[0]) + "</td><td>" + row[1] + "</td><td>" + row[2] + "</td><td>" \
                                + row[3] + "</td></tr>"
                response += "</table>"
            return response

        if param == "update":
            sleep(0.05)
            with sqlite3.connect(DB_STRING) as c:
                r = c.execute("SELECT * FROM benutzer")
                response = "<table width='100%' class='table table-striped table-bordered'" \
                           "cellspacing='0'><tr><td>Nr</td><td>Vorname</td><td>Nachname</td>" \
                           "<td>Username</td><td>Ändern</td></tr>"
                while True:
                    row = r.fetchone()
                    if row is None:
                        break
                    response += "<tr><td>" + str(row[0]) + "</td><td>" + row[1] + "</td><td>" + row[2] + "</td><td>" \
                                + row[3] + "</td><td> <button onClick='updateBenutzer(" + str(row[0]) + ")'>Ändern" \
                                "</button></td></tr>"
                response += '</table>'
            return response

        if param == "getBenutzer":
            with sqlite3.connect(DB_STRING) as c:
                r = c.execute("SELECT * FROM benutzer WHERE nr=" + input)
                while True:
                    row = r.fetchone()
                    if row is None:
                        break
                    response = str(row[0]) + "#" + row[1] + "#" + row[2] + "#" + row[3] + "#" + row[4];
            return response

        if param == "updateBenutzer":
            with sqlite3.connect(DB_STRING) as c:
                print(input)
                liste = input.split('#')
                c.execute("UPDATE benutzer SET vorname='" + liste[1] + "',nachname='"
                          + liste[2] + "',username='" + liste[3] + "',password='" + liste[4] + "' WHERE nr=" + liste[0])
                return "Benutzer erfolgreich geändert."

        if param == "create":
            with sqlite3.connect(DB_STRING) as c:
                liste = input.split('#')
                print(liste[0])
                c.execute("INSERT INTO benutzer(vorname, nachname, username, password) VALUES (" + liste[0] + ", "
                          + liste[1] + ", " + liste[2] + ", " + liste[3] + ")")
                return "Benutzer erfolgreich gespeichert."

        if param == "delete":
            with sqlite3.connect(DB_STRING) as c:
                r = c.execute("SELECT * FROM benutzer")
                response = "<table width='100%' class='table table-striped table-bordered'" \
                           "cellspacing='0'><tr><td>Nr</td><td>Vorname</td><td>Nachname</td>" \
                           "<td>Username</td><td>Löschen</td></tr>"
                while True:
                    row = r.fetchone()
                    if row is None:
                        break
                    response += "<tr><td>" + str(row[0]) + "</td><td>" + row[1] + "</td><td>" + row[2] + "</td><td>" \
                                + row[3] + "</td><td> <button onClick='deleteBenutzer(" + str(row[0]) + ")'>Löschen" \
                                "</button></td></tr>"
                response += '</table>'
            return response

        if param == "deleteBenutzer":
            with sqlite3.connect(DB_STRING) as c:
                c.execute("DELETE FROM benutzer WHERE nr=" + input)
            return self.POST("delete", "")

        return "error"


def setup_database():
    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE IF EXISTS benutzer")
        con.execute("CREATE TABLE IF NOT EXISTS benutzer(nr INTEGER PRIMARY KEY AUTOINCREMENT, vorname VARCHAR, "
                    "nachname VARCHAR, username VARCHAR, password VARCHAR)")
        con.execute("INSERT INTO benutzer VALUES(null,'Marvin', 'Ertl', 'mertl', 'password')")
        con.execute("INSERT INTO benutzer VALUES(null,'Lukas', 'Zuba', 'lzuba', 'password')")


def cleanup_database():
    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE IF EXISTS benutzer")


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.engine.subscribe('start', setup_database)
    cherrypy.engine.subscribe('stop', cleanup_database)
    cherrypy.config.update({'server.socket_port': 24128})
    cherrypy.config.update({'engine.autoreload_on': False})

    webapp = CRUD()
    webapp.generator = CRUDWebService()
    cherrypy.quickstart(webapp, '/', conf)
