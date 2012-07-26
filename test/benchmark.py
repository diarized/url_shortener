#!/usr/bin/env python

import threading
import requests
import time

REQUESTS = 4
THREADS = 2

class FetchUrl(threading.Thread):
    """ Thread class for requests requests """
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for i in xrange(REQUESTS):
            rr = requests.post('http://localhost:8888/', {'full_url':'http://www.google.com/'})
            print("request {0}, status_code {1}".format(i, rr.status_code))

def bench():
    """ Counts time """
    threads = []
    for i in xrange(THREADS):
        threads.append(FetchUrl())
    start_time = time.time()
    for i in xrange(THREADS):
        threads[i].start()
    for i in xrange(THREADS):
        threads[i].join()
    print(str(1000*(time.time() - start_time)/(THREADS*REQUESTS)) + 'ms')


if __name__ == '__main__':
    bench()

