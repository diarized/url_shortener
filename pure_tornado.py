#!/usr/bin/env python

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
from random import sample
from string import digits, ascii_letters
import cache

def short_id(num):
    """Creates random combination of letters and digits"""
    return "".join(sample(digits + ascii_letters, num))

class MainHandler(tornado.web.RequestHandler):
    """
    Class that serves in response to GET and POST requests
    """
    def get(self, short_url=''):
        """
        Responses to GET request, different if with short url
        """
        if short_url == '':
            self.render('index.html', page_title="URL shortener", body_id="", short_url="whatever", title="URLsh")
        else:
            self.redirect(str(cache.tcache.get_value(short_url)), permanent=True)

    def post(self, donotneedit):
        """
        Responses to POST request, stores new short URL
        """
        post_data = self.get_argument('new_url', 'No URL to short')
        print post_data
        id = short_id(NAMESPACE)
        tcache.put(id, post_data)
        cache.tcache.put(id, post_data)
        shortened_url = "/{0}".format(id)
        self.render('shurl.html', page_title='Shorted URL', short_url=shortened_url)


# Settings. Common for this pure Tornado implementation and for all
# derived (e.g. with gevent)
settings = {
    "static_path":os.path.join(os.path.dirname(__file__),'static'),
    "template_path":"templates",
}


if __name__ == "__main__":
    application = tornado.web.Application([(r"/(.*)", MainHandler),], **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

