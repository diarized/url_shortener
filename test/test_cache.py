#!/usr/bin/env python

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

import cache
import unittest

class TestCache(unittest.TestCase):
    def setUp(self):
        pass

    def test_cache(self):
        sent_key = "Ala"
        sent_value = "kot"
        cache.tcache.put(sent_key, sent_value)
        received = str(cache.tcache.get_value(sent_key))
        self.assertEqual(received, sent_value)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCache))

    return suite
if __name__ == '__main__':
    suiteFew = unittest.TestSuite()
    suiteFew.addTest(TestCache("test_cache"))
    #unittest.TextTestRunner(verbosity=2).run(suiteFew)
    unittest.TextTestRunner(verbosity=2).run(suite())
