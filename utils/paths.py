import os
from pathlib import Path


def get_data_path():
    path = Path(os.path.dirname(os.path.realpath(__file__)))

    return str(path.parent) + '/data'
