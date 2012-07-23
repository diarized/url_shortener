from cache import DbmDb as Cache
import time

class AbuseChecker(object):
    def __init__(self, delta):
        self.db = Cache('abuser')
        self.delta = delta

    def is_abuser(self, requester_ip):
        current_time = time.time()
        visited = self.db.get(requester_ip)
        if visited:
            if current_time - visited < self.delta:
                return True
        return False

