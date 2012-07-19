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
import cache
import time

def short_id(num):
    return "".join(sample(digits + ascii_letters, num))

with open('templates/index.html') as fh:
    index_template = fh.read()

with open('templates/shurl_twisted.html') as fh:
    shurl_template = fh.read()

class UrlShortener(Resource):  # Resources are what Site knows how to deal with
    isLeaf = True  # Disable child lookup

    def render_GET(self, request):
        if request.path == '/':
            #request.__class__ = twisted.web.server.Request
            cache.tcache.put(request.getClientIP, time.time())
            log.msg("Client IP: {0}".format(request.getClientIP()))
            return index_template
        else:
            short_url = request.path.lstrip('/')
            return redirectTo(str(cache.tcache.get_value(short_url)), request)

    def render_POST(self, request):  # Define a handler for POST requests
        full_url = cgi.escape(request.args["full_url"][0])
        url_id = short_id(5)
        log.msg("URL {0} ===> {1}".format(full_url, url_id))
        cache.tcache.put(url_id, full_url)
        return shurl_template.format(url_id)

log.startLogging(sys.stdout)
reactor.listenTCP(8888, Site(UrlShortener()))
reactor.run()


