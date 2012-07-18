#!/usr/bin/env python

import tornado.wsgi
import gevent.wsgi
import pure_tornado

application = tornado.wsgi.WSGIApplication([(r"/(.*)", pure_tornado.MainHandler),],
                **pure_tornado.settings)

if __name__ == "__main__":
    server = gevent.wsgi.WSGIServer(('', 8888), application)
    server.serve_forever()

