import os

def create_directory_if_it_does_not_exists(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    return 0