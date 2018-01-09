import os, os.path
import random
import sqlite3
import string
import time

import cherrypy

DB_STRING = "datenbank.db"


class CRUD(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')


@cherrypy.expose
class CRUDWebService(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        with sqlite3.connect(DB_STRING) as c:
            cherrypy.session['ts'] = time.time()
            r = c.execute("SELECT vorname FROM benutzer WHERE nr = 0", [cherrypy.session.id])
            return r.fetchone()

    def POST(self, length=8):
        print("TEST submit button")
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        with sqlite3.connect(DB_STRING) as c:
            cherrypy.session['ts'] = time.time()
            #c.execute("INSERT INTO user_string VALUES (?, ?)",
            #          [cherrypy.session.id, some_string])
            some_string = ""
            r = c.execute("SELECT vorname FROM benutzer WHERE nr = 0")
            print(r)
        return r.fetchone()

    def PUT(self, another_string):
        with sqlite3.connect(DB_STRING) as c:
            cherrypy.session['ts'] = time.time()
            c.execute("UPDATE user_string SET value=? WHERE session_id=?",
                      [another_string, cherrypy.session.id])

    def DELETE(self):
        cherrypy.session.pop('ts', None)
        with sqlite3.connect(DB_STRING) as c:
            c.execute("DELETE FROM user_string WHERE session_id=?",
                      [cherrypy.session.id])


def setup_database():
    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE IF EXISTS benutzer")
        con.execute("CREATE TABLE IF NOT EXISTS benutzer(nr INTEGER PRIMARY KEY, vorname VARCHAR, nachname VARCHAR, "
                    "username VARCHAR, password VARCHAR)")
        con.execute("INSERT INTO benutzer VALUES(0, 'Marvin', 'Ertl', 'mertl', 'password')")


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
    cherrypy.config.update({'server.socket_port': 8121})

    webapp = CRUD()
    webapp.generator = CRUDWebService()
    cherrypy.quickstart(webapp, '/', conf)
