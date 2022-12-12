import os


def get_dir_path(filename):
    real_path = os.path.realpath(filename)
    dir_path = os.path.dirname(real_path)

    return dir_path