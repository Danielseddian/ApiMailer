from django.shortcuts import render

from forms import ResolveForm
# from .models import Task, Solution
from tools import make_folder_name, check_directory, get_import, write_to_the_file

TASK_ID = [0]
TASK_TEXT = ""
TASK_TASK = ""
TASK_CODE = """def abra_cadabra(magic_book):
    return magic_book
"""
TASK_EXPECTED = ""

RESOLVE_ID = [0]
RESOLVE_RESOLVE = """def foo(magic_book):
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
    def __init__(self, name: str, text: str, task: str, code: str, expected: str, is_pub: bool) -> None:
        TASK_ID[0] += 1
        self.id = TASK_ID[0]
        self.name = name
        self.text = text
        self.task = task
        self.code = code
        self.expected = expected
        self.is_pub = is_pub

    def save(self):
        return self


class Resolve:
    def __init__(self, folder: str, user: User, task: Task, resolve: str) -> None:
        RESOLVE_ID[0] += 1
        self.id = RESOLVE_ID[0]
        self.folder = folder
        self.user = user
        self.task = task
        self.resolve = resolve

    def save(self):
        return self


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
    expected=TASK_EXPECTED,
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
        return render(request, 'index.html', {'form': form})
    #     new_post = form.save(commit=False)
    #     new_post.author = request.user
    #     new_post.save()
    if not resolve:
        resolve = Resolve(folder=make_folder_name(), user=request.user, task=task, resolve=form)
        resolve.save()
    file_name = "resolve"
    file_path = write_to_the_file("\n\n".join((task.code, resolve.resolve)), check_directory(resolve.folder), file_name)
    resolving = get_import(file_name, file_path)
    print(resolving.foo("✨ it's a magic time ✨"))
    return render(request, 'index.html', {'form': form})
