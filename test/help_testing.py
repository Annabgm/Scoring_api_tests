import functools


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