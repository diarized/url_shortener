#!/usr/bin/env python

import cherrypy
from random import sample
from string import digits, ascii_letters
import cgi
import cache
import time

def short_id(num):
    return "".join(sample(digits + ascii_letters, num))

with open('templates/cherry_index.html') as fh:
    index_template = fh.read()

with open('templates/cherry_shurl.html') as fh:
    shurl_template = fh.read()

class UrlShortener(object):
    def index(self):
        return index_template
    index.exposed = True

    def get(self, url_id):
        cherrypy.response.status = 302
        cherrypy.response.headers["location"] = str(cache.tcache.get_value(url_id))
    get.exposed = True

    def post(self, full_url, submit):
        url_id = short_id(5)
        cache.tcache.put(url_id, full_url)
        return shurl_template.format(url_id)
    post.exposed = True

cherrypy.root = UrlShortener()
cherrypy.config.update(file = 'cherry_server.cfg')
cherrypy.server.start()


