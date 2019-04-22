import os


class Config(object):
    def __getattr__(self, item):
        return os.environ.get(item)
