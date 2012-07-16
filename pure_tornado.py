#!/usr/bin/env python

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
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

class MainHandler(tornado.web.RequestHandler):
    def get(self, short_url=''):
        if short_url == '':
            self.render('index.html', page_title="URL shortener", body_id="", short_url="whatever", title="URLsh")
        else:
            self.redirect(str(tcache.get_value(short_url)), permanent=True)

    def post(self, nothing):
        post_data = self.get_argument('new_url', 'No URL to short')
        print post_data
        id = short_id(5)
        tcache.put(id, post_data)
        shortened_url = "http://localhost:8888/{0}".format(id)
        self.render('shurl.html', page_title='Shorted URL', short_url=shortened_url)


settings = {
    "static_path":os.path.join(os.path.dirname(__file__),'static'),
    "template_path":"templates",
}

application = tornado.web.Application([(r"/(.*)", MainHandler),], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

