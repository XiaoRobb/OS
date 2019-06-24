from enum import Enum
from Fifth.Global import CPUInstruction
from Fifth.Global import Semaphore


class ProcessType(Enum):
    Producer = 1
    Consumer = 2


class Process:

    def __init__(self, person_type, run_times):
        self.person_type = person_type
        self.instructions = []
        self.run_times = run_times
        if person_type == ProcessType.Producer:
            self.instructions.append((CPUInstruction.PRODUCE, -1))
            self.instructions.append((CPUInstruction.P, Semaphore.Empty))
            self.instructions.append((CPUInstruction.PUT, -1))
            self.instructions.append((CPUInstruction.V, Semaphore.Full))
            self.instructions.append((CPUInstruction.GOTO, 0))
            self.process_name = "Producer"
            self.print_holder = ""
        else:
            self.instructions.append((CPUInstruction.P, Semaphore.Full))
            self.instructions.append((CPUInstruction.GET, -1))
            self.instructions.append((CPUInstruction.V, Semaphore.Empty))
            self.instructions.append((CPUInstruction.CONSUME, -1))
            self.instructions.append((CPUInstruction.GOTO, 0))
            self.process_name = "Consumer"
            self.print_holder = "\t\t\t\t\t\t"
        self.instructions_num = len(self.instructions)

