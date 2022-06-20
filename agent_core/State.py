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

    @classmethod
    def __getitem__(cls, key):
        try:
            return cls[key]
        except KeyError as e:
            raise TypeError() from e

    def __str__(self):
        return super().__str__().lstrip("State.")

    def __repr__(self):
        return super().__str__()

    def __lt__(self, other):
        if isinstance(other, State):
            return self.value < other.value
        else:
            raise TypeError("'<' not supported between instances of 'State' "
                            "and '{}'".format(type(other).__name__))

    def __le__(self, other):
        if isinstance(other, State):
            return self.value <= other.value
        else:
            raise TypeError("'<=' not supported between instances of 'State' "
                            "and '{}'".format(type(other).__name__))

    def __ge__(self, other):
        if isinstance(other, State):
            return self.value >= other.value
        else:
            raise TypeError("'>=' not supported between instances of 'State' "
                            "and '{}'".format(type(other).__name__))

    def __gt__(self, other):
        if isinstance(other, State):
            return self.value > other.value
        else:
            raise TypeError("'>' not supported between instances of 'State' "
                            "and '{}'".format(type(other).__name__))
