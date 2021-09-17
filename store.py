import time
import redis


class RedisStore(object):
    def __init__(self, host, port, db_store=0, db_cache=1):
        self.host = host
        self.port = port
        self.timeout = 5
        self.db_store = db_store
        self.db_cache = db_cache
        self.retry = 5
        self.store = None
        self.cache = None
        self.connect(type_st='store')
        self.connect(type_st='cache')

    def connect(self, type_st='store'):
        if type_st == 'store':
            self.store = redis.StrictRedis(
                host=self.host,
                port=self.port,
                db=self.db_store,
                socket_timeout=self.timeout
            )
        elif type_st == 'cache':
            self.cache = redis.StrictRedis(
                host=self.host,
                port=self.port,
                db=self.db_cache,
                socket_timeout=self.timeout
            )

    def try_command(self, type_st='store'):
        if type_st == 'store':
            obj = self.store
        elif type_st == 'cache':
            obj = self.cache
        else:
            raise NotImplementedError('The type of store {} not found'.format(type))

        count = 0
        while True:
            try:
                obj.ping()
                return True
                # return f(*args, **kwargs)
            except redis.exceptions.ConnectionError:
                count += 1

                # re-raise the ConnectionError if we've exceeded max_retries
                if count > self.retry:
                    return False

                backoff = count * 5

                print('Retrying in {} seconds'.format(backoff))
                time.sleep(backoff)

                self.connect(type_st=type_st)

    def cache_set(self, key, value, save_time):
        if self.try_command(type_st='cache'):
            try:
                self.cache.set(key, value, ex=save_time)
            except:
                return None

    def cache_get(self, key):
        if self.try_command(type_st='cache'):
            try:
                val = int(self.cache.get(key).decode("utf-8"))
                return val
            except:
                return None

    def get(self, key):
        if self.try_command(type_st='store'):
            try:
                val = self.store.get(key).decode("utf-8")
                return val
            except redis.ConnectionError:
                raise ConnectionError('Connection no more established.')
        else:
            raise ConnectionError('Connection no more established.')