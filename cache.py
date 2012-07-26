import os
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

DEBUG = True
CACHE_SIZE = 3000

dot = os.path.dirname(__file__)

class DbmDb(object):
    def __init__(self, name, cache_type='file'):
        self._cache_opts = {
            'cache.type': cache_type,
            'cache.data_dir': os.path.join(dot,'{0}_data'.format(name)),
            'cache.lock_dir': os.path.join(dot,'{0}_lock'.format(name)),
        }
        self.db = CacheManager(**parse_cache_config_options(self._cache_opts))
        self.tdb = self.db.get_cache("stuff", type='dbm') #, expire=3600)
        self._cache = {}

    def put(self, key, value):
        if not self._cache.has_key(key):
            if DEBUG:
                print('IP not in cache. Adding')
            self._cache[key] = value
        if DEBUG:
            print('IP already in cache. Needs an update.')
        self._update_cache(key, value)
        self.tdb.put(key, value)

    def get(self, key):
        value = self._cache.get(key)
        if not value:
            try:
                value = self.tdb.get_value(key)
            except KeyError:
                return False
        return value

    def _update_cache(self, key, value):
        current_cache_size = len(self._cache)
        if current_cache_size > CACHE_SIZE:
            raise ValueError(
                    "Cache length = {0}. It is bigger then fixed {1} elements.".format(
                        current_cache_size,
                        CACHE_SIZE))
        if current_cache_size == CACHE_SIZE:
            if DEBUG:
                print('Cache is {0} long.'.format(current_cache_size))
            oldest = self._cache.keys()[0]
            self._cache.pop(oldest)
            if DEBUG:
                print('Key "{0}" deleted.'.format(oldest))
                print('After deletion the cache is {0} long.'.format(current_cache_size))
        self._cache[key] = value
        if DEBUG:
            print('After adding the cache is {0} long.'.format(current_cache_size))

