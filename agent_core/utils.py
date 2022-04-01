# This file is part of TCC
# Copyright (C) 2022  Natan Junges <natanjunges@alunos.utfpr.edu.br>
#
# TCC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# TCC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TCC.  If not, see <https://www.gnu.org/licenses/>.

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
