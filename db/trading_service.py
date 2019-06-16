from db import get_collection

keynote = get_collection('keynote', 'trading')


def insert(data):
    keynote.insert(data)


def find(*args, **kwargs):
    return keynote.find(*args, **kwargs)


def find_one(*args, **kwargs):
    return keynote.find_one(*args, **kwargs)


def update(key, query, upsert=True, multiline=False):
    return keynote.update(key, query, upsert, multiline)


def remove(query):
    return keynote.remove(query)

