import time
import redis
import logging
import random


param_store = {'host': '127.0.0.1',
               'port': 6379,
               'bd': 0,
               'timeout': 5}

param_cache = {'host': '127.0.0.1',
               'port': 6379,
               'bd': 1,
               'timeout': 5}


class RedisStore(object):
    def __init__(self, host, port, bd, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.bd = bd
        self.retry = 5
        self.cap = 5
        self.store = None

    def connect(self):
        self.store = redis.StrictRedis(
                host=self.host,
                port=self.port,
                db=self.bd,
                socket_timeout=self.timeout
            )

    def try_command(self):
        count = 0
        while True:
            try:
                self.store.ping()
                return True
            except redis.exceptions.ConnectionError:
                count += 1

                # re-raise the ConnectionError if we've exceeded max_retries
                if count > self.retry:
                    return False

                backoff = random.uniform(0, min(self.cap, pow(2, count)*0.1))

                logging.info('Retrying in {} seconds'.format(backoff))
                time.sleep(backoff)

                self.connect()

    def set(self, key, value, save_time):
        if self.try_command():
            try:
                self.store.set(key, value, ex=save_time)
            except:
                return None

    def get(self, key):
        if self.try_command():
            try:
                val = self.store.get(key)
                if val is None:
                    return
                else:
                    return val.decode("utf-8")
            except redis.ConnectionError:
                raise ConnectionError('Connection no more established.')
        else:
            raise ConnectionError('Connection no more established.')


class RedisCache(object):
    def __init__(self, host, port, bd, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.bd = bd
        self.retry = 5
        self.cap = 5
        self.store = None

    def connect(self):
        self.store = redis.StrictRedis(
                host=self.host,
                port=self.port,
                db=self.bd,
                socket_timeout=self.timeout
            )

    def try_command(self):
        count = 0
        while True:
            try:
                self.store.ping()
                return True
            except redis.exceptions.ConnectionError:
                count += 1

                # re-raise the ConnectionError if we've exceeded max_retries
                if count > self.retry:
                    return False

                backoff = random.uniform(0, min(self.cap, pow(2, count)*0.1))

                logging.info('Retrying in {} seconds'.format(backoff))
                time.sleep(backoff)

                self.connect()

    def set(self, key, value, save_time):
        if self.try_command():
            try:
                self.store.set(key, value, ex=save_time)
            except:
                return None

    def get(self, key):
        if self.try_command():
            try:
                val = self.store.get(key)
                if val is None:
                    return
                else:
                    return int(val.decode("utf-8"))
            except redis.ConnectionError:
                return
        else:
            return


stores = {'store': RedisStore(**param_store),
          'cache': RedisCache(**param_cache)}
