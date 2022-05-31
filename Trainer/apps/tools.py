import string
import secrets
import os
from Trainer.settings import MEDIA_ROOT
import importlib


def make_folder_name(prefix="temp_", symbols=string.ascii_letters + string.digits, length=10):
    return prefix + "".join(secrets.choice(symbols) for _ in range(length))


def check_directory(folder_name=None, base_directory=MEDIA_ROOT):
    if not folder_name:
        folder_name = make_folder_name()
    directory = "\\".join((base_directory, folder_name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def write_to_the_file(data, directory=None, file_name="py_file"):
    if not directory:
        directory = check_directory()
    path = "\\".join((directory, file_name + ".py"))
    with open(path, "w", encoding="UTF-8") as file:
        file.write(data)
    return path


def get_import(module_name, directory):
    spec = importlib.util.spec_from_file_location(module_name, directory)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_resolve(task, resolve):
    file_name = "resolve"
    file_path = write_to_the_file("\n\n".join((task.code, resolve.resolve)), check_directory(resolve.folder), file_name)
    result = []
    for data in task.data:
        try:
            resolving = get_import(file_name, file_path)
            getattr(resolving, task.call)(data)
            result.append(getattr(resolving, "get_result")())
        except Exception as exc:
            result.append(exc)
    return result
