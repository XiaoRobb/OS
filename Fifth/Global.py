from enum import Enum
import random


class Semaphore(Enum):
    Empty = 1
    Full = 2


class CPUInstruction(Enum):
    P = 0
    V = 1
    PUT = 2
    GET = 3
    PRODUCE = 4
    CONSUME = 5
    GOTO = 6
    NOP = 7


class Glo:
    pc = 0
    empty = 10
    full = 0
    products = [''for _ in range(10)]
    products_in_pointer = 0
    products_out_pointer = 0
    product_in = ''
    product_out = ''

    running_process = None
    runable_processes = []
    waiting_processes_for_empty = []
    waiting_processes_for_full = []
    end_processes = []
    process_with_pcbs = []

    @staticmethod
    def wake_process_for_empty():
        index = random.randint(0, len(Glo.waiting_processes_for_empty)-1)
        Glo.runable_processes.append(Glo.waiting_processes_for_empty[index])
        Glo.waiting_processes_for_empty.pop(index)

    @staticmethod
    def wake_process_for_full():
        index = random.randint(0, len(Glo.waiting_processes_for_full) - 1)
        Glo.runable_processes.append(Glo.waiting_processes_for_full[index])
        Glo.waiting_processes_for_full.pop(index)



