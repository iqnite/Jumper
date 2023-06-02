# Functions for score management

def sort(lst):
    if len(lst) < 1:
        return lst

    # Clean list from invalid lines
    for l in range(len(lst)):
        try:
            if not (':' in lst[l]):
                del lst[l]
            if lst[l] == '\n':
                del lst[l]
        except:
            pass

    for j in range(len(lst)):
        for k in range(len(lst)-1):
            item1 = lst[k]
            item1t = float((item1.split(':')[1]))
            if k != len(lst)-1:
                item2 = lst[k+1]
                item2t = float((item2.split(':')[1]))
                if item1t < item2t:
                    # Swap items
                    lst[k] = str(item2)
                    lst[k+1] = str(item1)

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


def top(f, n, s):
    try:
        file = open(f, 'r')
    except:
        file = open(f, 'x')
        scores = []
    else:
        scores = file.readlines()
    finally:
        if n != "" and n != None:
            scores.append(f"{n}:{s}")
        scores = sort(scores)
        file = open(f, 'w')
        for i in scores:
            file.write(str(i).strip('\n') + '\n')
        file.flush()
        file.close()


def get(f):
    try:
        fobj = open(f, 'r')
    except:
        return [""]
    else:
        lst = fobj.readlines()
        fobj.close()
        return lst
