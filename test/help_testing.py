import functools
import hashlib
from datetime import datetime

import api


def cases(case):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in case:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                try:
                    f(*new_args)
                except Exception as e:
                    msg = 'Case has failed with attributes:: ' + ', '.join('{}: {}'.format(k, v) for k, v in c.items())
                    print(msg)
                    raise e
        return wrapper
    return decorator


def set_valid_auth(request):
    if request.get("login") == api.ADMIN_LOGIN:
        request["token"] = hashlib.sha512((datetime.now().strftime("%Y%m%d%H") +
                                           api.ADMIN_SALT).encode('utf-8')).hexdigest()
    else:
        msg = str(request.get("account", "")) + str(request.get("login", "")) + api.SALT
        request["token"] = hashlib.sha512(msg.encode('utf-8')).hexdigest()


def get_store_cache_key(request):
    arg = request['arguments']
    key_parts = [
        arg.get('first_name', ""),
        arg.get('last_name', ""),
        str(arg.get('phone', "")),
        datetime.strptime(arg['birthday'], '%d.%m.%Y').strftime("%Y%m%d") if 'birthday' in arg.keys() else "",
    ]
    key = "uid:" + hashlib.md5("".join(key_parts).encode('utf-8')).hexdigest()
    return key