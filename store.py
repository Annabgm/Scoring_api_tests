from datetime import datetime
import random
import time
import json

class MockStore(object):
    def __init__(self, server):
        self.store_cache = {}
        self.server = server

    def connect(self):
        if self.server.connected:
            return True
        else:
            self.server.request()
            if self.server.connected:
                return True
            return False


    def cache_set(self, key, value, save_time):
        cache_time = datetime.now().timestamp() + save_time
        connected = self.connect()
        if connected:
            self.store_cache[key] = (cache_time, value)
        return

    def cache_get(self, key):
        request_time = datetime.now().timestamp()
        connected = self.connect()
        value = None
        if connected:
            try:
                time_set, value = self.store_cache[key]
            except KeyError:
                pass
            else:
                if time_set < request_time:
                    del self.store_cache[key]
                    value = None
        return value

    def get(self, key):
        connected = self.connect()
        if not connected:
            raise ConnectionError('MokeStore emulating a connection error')
        key_seed = key.split(':')[-1]
        random.seed(key_seed)
        interests = ["cars", "pets", "travel", "hi-tech", "sport", "music", "books", "tv", "cinema", "geek", "otus"]
        return json.dumps(random.sample(interests, 2))


class MockStoreConnection(object):
    def __init__(self, connected=True, probability=0.5):
        self.connected = connected
        self.connect_prob = probability
        self.timeout = 1
        self.attemps_lim = 10

    def request(self):

        if not self.connected:
            attemps = 0
            value = False
            while attemps < self.attemps_lim:
                if random.random() > self.connect_prob:
                    value = True
                    break
                else:
                    print(attemps)
                    attemps += 1
                    print('Try to reconnect.')
                    time.sleep(self.timeout)
            self.connected = value
