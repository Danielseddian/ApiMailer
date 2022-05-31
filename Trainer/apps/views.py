from datetime import datetime as dt
from django.shortcuts import render

from .forms import ResolveForm
# from .models import Task, Solution
from .tools import make_folder_name, check_resolve

TASK_ID = [0]
TASK_TEXT = """Ирина Гренкина учится в школе программирования и является лучшей ученицей курса, у неё по всем предметам оценки только: «Отлично». Недавно ей дали сложное домашнее задание: вместе с друзьями написать программу, которая состоит из нескольких частей.

Друзья договорились, что каждый будет писать свою часть, но Ирина знает, что у Ромы Слизнева треснула клавиатура, поэтому иногда он допускает ошибки, пропуская некоторые буквы. А поменять клавиатуру Рома не решается, потому что для этого необходимо пойти к школьному завхозу, Филипу Августовичу, который отличается скверным характером.

Ирина предложила Слизневу посмотреть его функцию, abra_cadabra(), и исправить ошибки, если они есть, но он отказался, потому что считает, что Гренкина снова будет читать ему нотации. Тогда подруга решила схитрить и написать свою версию Роминой функции, которая будет называться focus_pocus(), а чтобы проучить друга, ей нужно сначала вызвать его функцию и, если она выдаст ошибку, напечатать об этом сообщение: «Рома, у тебя в программе ошибка!».

Так как у Ромы не печатаются некоторые буквы, то точно возникнет ошибка «KeyError», когда он попытается извлечь значения из словаря magic_dictionary. Ирина слишком занята, поэтому попросила вас написать небольшой код, чтобы проверить функцию abra_cadabra() и напечатать предупреждение, если возникнет ошибка, а затем вызвать её функцию, focus_pocus().
"""

TASK_TASK = "Написать функцию make_magic_replace(), которая принимает словарь magic_dictionary, вызывавет функцию abra_cadabra() и передаёт в неё этот словарь. Если работа функции вызывает ошибку KeyError необходимо перехватить её, напечатать сообщение «Рома, у тебя в программе ошибка!» и вызывать функцию focus_pocus() и передать словарь в неё."
TASK_CODE = """result = [0, 0]
magic_book = {"leviosa": 1, "avis": 2, "lumos": 3, "descendo": 4}

def print(string):
    if string == "Рома, у тебя в программе ошибка!":
        result[1] = 1
    else:
        result[1] = 2


def get_result():
    return result


def abra_cadabra(i):
    keys = ["lefiosa", "avis", "lumos", "desendo"]
    magic_book[keys[i]]
    result[0] = 1


def focus_pocus(i):
    keys = ["leviosa", "avis", "lumos", "descendo"]
    magic_book[keys[i]]
    result[0] = 2
"""
TASK_CALL = "make_magic_replace"
TASK_DATA = [1, 0, 2]

RESOLVE_ID = [0]
RESOLVE_RESOLVE = """def make_magic_replace(magic_book):
    return abra_cadabra(magic_book)
"""
RESOLVE_FOLDER = "temp_WAjJuCuL5f"

USER_ID = [0]


class User:
    def __init__(self, username: str) -> None:
        USER_ID[0] += 1
        self.id = USER_ID[0]
        self.username = username

    def save(self):
        return self


class Task:
    def __init__(self, name: str, text: str, task: str, code: str, call: str, data: dict, is_pub: bool) -> None:
        TASK_ID[0] += 1
        self.id = TASK_ID[0]
        self.name = name
        self.text = text
        self.task = task
        self.code = code
        self.call = call
        self.data = data
        self.is_pub = is_pub

    def save(self):
        return self


class Resolve:
    def __init__(self, folder: str, user: User, task: Task, resolve: str, date=dt.now()) -> None:
        RESOLVE_ID[0] += 1
        self.id = RESOLVE_ID[0]
        self.folder = folder
        self.user = user
        self.task = task
        self.date = date
        self.resolve = resolve

    def save(self):
        return self

    def update(self, folder=None, user=None, task=None, resolve=None, date=dt.now()):
        self.folder = folder or self.folder
        self.user = user or self.user
        self.task = task or self.task
        self.resolve = resolve or self.resolve


class Request:
    def __init__(
        self,
        user: User,
        data: dict,
    ) -> None:
        self.user = user
        self.data = data


USER = User(username="Someone")
TASK = Task(
    name="Сломанная клавиатура и небольшая ошибка.",
    code=TASK_CODE,
    text=TASK_TEXT,
    task=TASK_TASK,
    call=TASK_CALL,
    data=TASK_DATA,
    is_pub=True,
)
REQUEST = Request(user=USER, data={"task": TASK})
RESOLVE = Resolve(folder=RESOLVE_FOLDER, user=USER, task=TASK, resolve=RESOLVE_RESOLVE)


def index(request):
    # _____to_do_____ #
    resolve = RESOLVE
    # --------------- #
    # _____to_do_____ #
    task = TASK
    # --------------- #
    form = ResolveForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'index.html', {'form': form, "page": [task]})
    if not resolve:
        resolve = Resolve(folder=make_folder_name(), user=request.user, task=task)
        resolve.save()
    resolve.update(resolve=form.data["resolve"], date=dt.now())
    print(check_resolve(task, resolve))
    return render(request, 'index.html', {'form': form, "page": [task]})
