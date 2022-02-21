from enum import Enum, auto

class Message(Enum):
    Integer = auto()
    String = auto()
    Boolean = auto()
    IntegerQuestion = auto()
    StringQuestion = auto()

    @classmethod
    def fromString(cls, str):
        if str == "True":
            return cls.Boolean
        elif str[-1] == "?":
            try:
                int(str[:-1])
                return cls.IntegerQuestion
            except:
                return cls.StringQuestion
        else:
            try:
                int(str)
                return cls.Integer
            except:
                return cls.String
