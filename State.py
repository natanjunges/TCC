from enum import Enum, auto

class State(Enum):
    Start = auto()

    TransmitReferent = auto()
    RequestReferentConfirmation1 = auto()
    RequestReferentConfirmation2 = auto()
    ConfirmReferent = auto()
    TransmitWord = auto()
    RequestWordConfirmation1 = auto()
    RequestWordConfirmation2 = auto()
    ConfirmWord1 = auto()
    ConfirmWord2 = auto()

    TransmitInducedReferent = auto()
    RequestInducedReferentConfirmation1 = auto()
    RequestInducedReferentConfirmation2 = auto()
    ConfirmInducedReferent = auto()
    RequestInductionConfirmation1 = auto()
    RequestInductionConfirmation2 = auto()
    ConfirmInduction1 = auto()
    ConfirmInduction2 = auto()

    End = auto()

    TR = TransmitReferent
    RRC1 = RequestReferentConfirmation1
    RRC2 = RequestReferentConfirmation2
    CR = ConfirmReferent
    TW = TransmitWord
    RWC1 = RequestWordConfirmation1
    RWC2 = RequestWordConfirmation2
    CW1 = ConfirmWord1
    CW2 = ConfirmWord2

    TIR = TransmitInducedReferent
    RIRC1 = RequestInducedReferentConfirmation1
    RIRC2 = RequestInducedReferentConfirmation2
    CIR = ConfirmInducedReferent
    RIC1 = RequestInductionConfirmation1
    RIC2 = RequestInductionConfirmation2
    CI1 = ConfirmInduction1
    CI2 = ConfirmInduction2

    FirstInteraction = TransmitReferent
    SecondInteraction = TransmitInducedReferent

    def __str__(self):
        return super().__str__().lstrip("State.")

    def __repr__(self):
        return super().__str__()

    def __lt__(self, other):
        if isinstance(other, State):
            return self.value < other.value
        else:
            raise TypeError("'<' not supported between instances of 'State' and '{}'".format(type(other).__name__))

    def __le__(self, other):
        if isinstance(other, State):
            return self.value <= other.value
        else:
            raise TypeError("'<=' not supported between instances of 'State' and '{}'".format(type(other).__name__))

    def __ge__(self, other):
        if isinstance(other, State):
            return self.value >= other.value
        else:
            raise TypeError("'>=' not supported between instances of 'State' and '{}'".format(type(other).__name__))

    def __gt__(self, other):
        if isinstance(other, State):
            return self.value > other.value
        else:
            raise TypeError("'>' not supported between instances of 'State' and '{}'".format(type(other).__name__))
