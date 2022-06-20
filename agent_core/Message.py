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

from enum import Enum, auto

class Message(Enum):
    Integer = auto()
    String = auto()
    Boolean = auto()
    IntegerQuestion = auto()
    StringQuestion = auto()

    @classmethod
    def fromString(cls, str_):
        if str_ == "True":
            return cls.Boolean
        elif str_[-1] == "?":
            try:
                int(str_[:-1])
                return cls.IntegerQuestion
            except:
                return cls.StringQuestion
        else:
            try:
                int(str_)
                return cls.Integer
            except:
                return cls.String
