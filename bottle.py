#!/usr/bin/env python

# shorty.py - simple URL shortener WSGI app with Beaker cache backend
# (c) Copyright 2010 Aleksandar Radulovic. All Rights Reserved.

import bottle
import webob
from random import sample
from string import digits, ascii_letters
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/url_shortener_data',
    'cache.lock_dir': '/tmp/url_shortener_lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))
tcache = cache.get_cache("stuff", type='dbm') #, expire=3600)

def short_id(num):
    return "".join(sample(digits + ascii_letters, num))

@bottle.route('/', method='GET')
def newurl():
    return bottle.static_file('index.html', root='/home/artur/Scripts/Python/url_shortener/bottle')

@bottle.route('/', method='POST')
def post():
    url = bottle.request.forms.new_url
    id = short_id(5)
    tcache.put(id, url)
    shortened_url = "http://localhost:8080/{0}".format(id)
    return '<a href="{0}">{0}</a>'.format(id)

@bottle.route('/<short>', method="GET")
def query(short):
    if tcache.has_key(short):
        return bottle.redirect(str(tcache.get_value(short)))
    else:
        return bottle.abort(404, "not found, sorry")

bottle.run(host='localhost', port=8080)

