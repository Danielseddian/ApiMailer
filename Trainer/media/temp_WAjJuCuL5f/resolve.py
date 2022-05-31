result = [0, 0]
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


def make_magic_replace(magic_book):
    try:
        abra_cadabra(magic_book)
    except KeyError:
        print("Рома, у тебя в программе ошибка!")
        focus_pocus(magic_book)
