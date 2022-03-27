def insert(list, item):
    i = 0
    l = len(list)
    li = None

    while i < l:
        li = list[i]

        if li < item:
            i += 1
        else:
            break

    if i == l or li != item:
        list.insert(i, item)
        return True
    else:
        return False

def merge(list1, list2):
    i = 0
    l = len(list2)
    j = 0

    while i < l:
        li = None
        item = list2[i]

        while j < len(list1):
            li = list1[j]

            if li < item:
                j += 1
            else:
                break

        if j == len(list1):
            list1 += list2[i:]
            break
        elif li != item:
            list1.insert(j, item)

        j += 1
        i += 1

def sub(list1, list2):
    i = 0
    l = len(list2)
    j = 0

    while i < l:
        li = None
        item = list2[i]

        while j < len(list1):
            li = list1[j]

            if li < item:
                j += 1
            else:
                break

        if j == len(list1):
            break
        elif li == item:
            list1.pop(j)

        i += 1
