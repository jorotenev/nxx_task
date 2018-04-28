import os


def get_directory_of_file(file):
    return os.path.dirname(os.path.realpath(file))
