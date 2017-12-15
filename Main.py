import cherrypy
import psycopg2

class HelloWorld(object):

    def index(self):
        conn = psycopg2.connect("dbname='xplorg' user='xplorg' host='xplorg.at' password='GCUNyNxsBHLZwRPV3ayeSYMS'")
        cur = conn.cursor()
        cur.execute("Select * from Person")
        rows = cur.fetchall()
        res = "Hello World! <br>"
        for row in rows:
            print(row)
            res += str(row)

        return res

    index.exposed = True


cherrypy.quickstart(HelloWorld())