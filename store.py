import time
import redis


param_store = {'host': '127.0.0.1',
               'port': 6379,
               'bd': 0}

param_cache = {'host': '127.0.0.1',
               'port': 6379,
               'bd': 1}


class RedisStore(object):
    def __init__(self, host, port, bd, type_bd):
        self.host = host
        self.port = port
        self.timeout = 5
        self.bd = bd
        self.retry = 5
        self.store = None
        self.connect()
        self.type_bd = type_bd

    @classmethod
    def from_args(cls, arg_dict, type_bd):
        arg_dict.update({'type_bd': type_bd})
        return cls(**arg_dict)

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
                # return f(*args, **kwargs)
            except redis.exceptions.ConnectionError:
                count += 1

                # re-raise the ConnectionError if we've exceeded max_retries
                if count > self.retry:
                    return False

                backoff = count * 5

                print('Retrying in {} seconds'.format(backoff))
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
                elif self.type_bd == 'cache':
                    return int(val.decode("utf-8"))
                else:
                    return val.decode("utf-8")
            except redis.ConnectionError:
                if self.type_bd == 'store':
                    raise ConnectionError('Connection no more established.')
                return
        else:
            if self.type_bd == 'store':
                raise ConnectionError('Connection no more established.')
            return


stores = {'store': RedisStore.from_args(param_store, 'store'),
          'cache': RedisStore.from_args(param_cache, 'cache')}
