import os
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

CACHE_SIZE = 3000

dot = os.path.dirname(__file__)

class DbmDb(object):
    def __init__(self, name, cache_type='file'):
        self.cache_opts = {
            'cache.type': cache_type,
            'cache.data_dir': os.path.join(dot,'{0}_data'.format(name)),
            'cache.lock_dir': os.path.join(dot,'{0}_lock'.format(name)),
        }
        self.db = CacheManager(**parse_cache_config_options(self.cache_opts))
        self.tdb = self.db.get_cache("stuff", type='dbm') #, expire=3600)
        self.cache = {}

    def put(self, key, value):
        if not self.cache.has_key(key):
            if len(self.cache) == CACHE_SIZE:
                oldest = self.cache.keys[0]
                self.cache.pop(oldest)
            self.cache[key] = value
        self.tdb.put(key, value)

    def get(self, key):
        value = self.cache.get(key)
        if value:
            return value
        else:
            return self.tdb.get_value(key)

