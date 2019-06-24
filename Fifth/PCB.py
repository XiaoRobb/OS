from enum import Enum


class PCBState(Enum):
    Runable = 1
    Running = 2
    Waiting = 3
    End = 4


class PCBWaitingReason(Enum):
    ReasonEmpty = 1
    ReasonFull = 2
    ReasonN = 3


class PCB:
    num = 0

    def __init__(self):
        self.state = PCBState.Runable
        self.id = PCB.num
        self.reason = PCBWaitingReason.ReasonN
        self.breakpoint = -1
