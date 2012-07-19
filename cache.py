import os
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': os.path.join(os.path.dirname(__file__),'url_shortener_data'),
    'cache.lock_dir': os.path.join(os.path.dirname(__file__),'url_shortener_lock'),
}

cache = CacheManager(**parse_cache_config_options(cache_opts))
tcache = cache.get_cache("stuff", type='dbm') #, expire=3600)


abuse_opts = {
    'cache.type': 'file',
    'cache.data_dir': os.path.join(os.path.dirname(__file__),'abuser_data'),
    'cache.lock_dir': os.path.join(os.path.dirname(__file__),'abuser_lock'),
}

abuse = CacheManager(**parse_cache_config_options(abuse_opts))
tabuse = cache.get_cache("abuse", type='dbm' , expire=5)

