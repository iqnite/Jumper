"""
Functions for score management
"""


def sort(lst):
    if len(lst) < 1:
        return lst

    # Clean list from invalid lines
    for i, line in enumerate(lst):
        try:
            if not ":" in line:
                del lst[i]
            if line == "\n":
                del lst[i]
        except IndexError:
            pass

    for _ in range(len(lst)):
        for k in range(len(lst) - 1):
            item1 = lst[k]
            item1t = float((item1.split(":")[1]))
            if k != len(lst) - 1:
                item2 = lst[k + 1]
                item2t = float((item2.split(":")[1]))
                if item1t < item2t:
                    # Swap items
                    lst[k] = str(item2)
                    lst[k + 1] = str(item1)

    # Remove duplicates
    names = []
    h = 0
    while h < len(lst):
        s = lst[h].split(":")
        if s[0] in names:
            del lst[h]
        else:
            names.append(s[0])
        h += 1
    return lst


def save(file_path, player_name, score):
    scores = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            scores = file.readlines()
    except FileNotFoundError:
        with open(file_path, "x", encoding="utf-8") as file:
            pass
    finally:
        if player_name:
            scores.append(f"{player_name}:{score}")
        scores = sort(scores)
        with open(file_path, "w", encoding="utf-8") as file:
            for i in scores:
                file.write(str(i).strip("\n") + "\n")


def get(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as fobj:
            return fobj.readlines()
    except FileNotFoundError:
        return [""]
