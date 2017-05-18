

def _long(value):
    try:
        return int(value)
    except NameError:  # we're Python 3, we don't have longs
        return int(value)
