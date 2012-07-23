#!/usr/bin/env python

import sys
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.util import redirectTo
from twisted.python import log
from random import sample
from string import digits, ascii_letters
import cgi
from cache import DbmDb as Cache
import time

ABUSE_INTERVAL = 5

def short_id(num):
    return "".join(sample(digits + ascii_letters, num))

with open('templates/index.html') as fh:
    index_template = fh.read()

with open('templates/shurl_twisted.html') as fh:
    shurl_template = fh.read()

class UrlShortener(Resource):  # Resources are what Site knows how to deal with
    isLeaf = True  # Disable child lookup

    def __init__(self):
        self.url_db = Cache('data')
        self.abuser_db = Cache('abuser')

    def render_GET(self, request):
        if request.path == '/':
            return index_template
        else:
            url_id = request.path.lstrip('/')
            return redirectTo(str(self.url_db.get(url_id)), request)

    def render_POST(self, request):  # Define a handler for POST requests
        if self.is_abuser(request):
            return index_template
        full_url = cgi.escape(request.args["full_url"][0])
        url_id = short_id(5)
        self.url_db.put(url_id, full_url)
        return shurl_template.format(url_id)

    def is_abuser(self, rq):
        client_ip = rq.getClientIP()
        try:
            last_time = float(self.abuser_db.get(client_ip))
        except:
            self.abuser_db.put(client_ip, float(time.time()))
            return False
        self.abuser_db.put(client_ip, float(time.time()))
        delta = time.time() - last_time
        if delta < ABUSE_INTERVAL:
            log.msg('Abuser from IP {0}'.format(client_ip))
            return True
        return False



log.startLogging(sys.stdout)
reactor.listenTCP(8888, Site(UrlShortener()))
reactor.run()


