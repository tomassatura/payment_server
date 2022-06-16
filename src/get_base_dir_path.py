import os


class GetBaseDirPath:
    def __call__(self):
        _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return _BASE_DIR
