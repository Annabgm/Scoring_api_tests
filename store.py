from datetime import datetime
import random
import time

class MonkStore(object):
    def __init__(self, server):
        self.store_cache = {}
        self.server = server

    def cache_set(self, key, value, save_time):
        cache_time = datetime.now().timestamp() + save_time
        if self.server.request:
            self.store_cache[key] = (cache_time, value)
        return

    def cache_get(self, key):
        request_time = datetime.now().timestamp()
        try:
            time_set, value = self.store_cache[key]
        except KeyError:
            value = None
        else:
            if time_set < request_time:
                value = None
            if not self.server.request:
                value = None
        return value

    def get(self, key):
        key_seed = key.split(':')[-1]
        random.seed(key_seed)
        interests = ["cars", "pets", "travel", "hi-tech", "sport", "music", "books", "tv", "cinema", "geek", "otus"]
        if not self.server.request:
            raise ConnectionError('MokeStore emulating a connection error')
        return '[' + ', '.join(random.sample(interests, 2)) + ']'


class MockStoreConnection(object):
    def __init__(self, connected=True, timeout=5):
        self.connected = connected
        self.timeout = timeout
        self.attemps_lim = 10

    @property
    def request(self):

        if self.connected == True:
            time.sleep(2)
            return True
        elif self.connected == False:
            attemps = 0
            value = False
            while attemps < self.attemps_lim:
                if random.random() > 0.8:
                    value = True
                    break
                else:
                    attemps += 1
                    print('Try to reconnect.')
                    time.sleep(self.timeout)
            return value
