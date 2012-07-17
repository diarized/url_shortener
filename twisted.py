#!/usr/bin/env python

from twisted.web.server import Site  # Site is a server factory for HTTP
from twisted.web.resource import Resource
from twisted.internet import reactor

class PrintPostBody(Resource):  # Resources are what Site knows how to deal with
    isLeaf = True  # Disable child lookup

    def render_POST(self, request):  # Define a handler for POST requests
        print request.content.read()  # Get the request body from this file-like object
        return "" # Define the response body as empty

reactor.listenTCP(8888, Site(PrintPostBody()))
reactor.run()



