#!/usr/bin/env python

import sys
from twisted.web.server import Site  # Site is a server factory for HTTP
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.util import redirectTo
from twisted.python import log
from random import sample
from string import digits, ascii_letters
import cgi
import cache

def short_id(num):
    return "".join(sample(digits + ascii_letters, num))


class UrlShortener(Resource):  # Resources are what Site knows how to deal with
    isLeaf = True  # Disable child lookup

    def render_GET(self, request):
        if request.path == '/':
            return '<html><body><form action="/" method="POST"><input name="full_url" type="text" /><input type="submit" name="submit" value="Submit" /></form></body></html>'
        else:
            short_url = request.path.lstrip('/')
            return redirectTo(str(cache.tcache.get_value(short_url)), request)

    def render_POST(self, request):  # Define a handler for POST requests
        full_url = cgi.escape(request.args["full_url"][0])
        url_id = short_id(5)
        log.msg("URL {0} ===> {1}".format(full_url, url_id))
        cache.tcache.put(url_id, full_url)
        return '<html><body><a href="/{0}">{0}</a><br /><a href="/">Home page</a></html></body>'.format(url_id)

log.startLogging(sys.stdout)
reactor.listenTCP(8888, Site(UrlShortener()))
reactor.run()


