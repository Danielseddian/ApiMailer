import string
import secrets
import os
from Trainer.settings import MEDIA_ROOT
import importlib


def make_temp_folder(prefix="temp_", symbols=string.ascii_letters + string.digits, length=10):
    return prefix + "".join(secrets.choice(symbols) for _ in range(length))


def check_or_make_directory(folder=make_temp_folder(), base_directory=MEDIA_ROOT):
    directory = "\\".join((base_directory, folder))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def get_import(module_name, directory):
    spec = importlib.util.spec_from_file_location(module_name, directory)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_to_the_file(data, directory=check_or_make_directory(), file_name="py_file"):
    path = "\\".join((directory, file_name + ".py"))
    with open(path, "w", encoding="UTF-8") as file:
        file.write(data)
    return path
