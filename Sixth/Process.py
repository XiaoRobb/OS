from enum import Enum
from Sixth.Global import CPUInstruction
from Sixth.Global import Semaphore


class ProcessType(Enum):
    Producer = 1
    Consumer = 2


class Process:
    producer_num = 0
    consumer_num = 0

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
            Process.producer_num += 1
            self.process_name = "Producer_"+str(Process.producer_num)
        else:
            self.instructions.append((CPUInstruction.P, Semaphore.Full))
            self.instructions.append((CPUInstruction.GET, -1))
            self.instructions.append((CPUInstruction.V, Semaphore.Empty))
            self.instructions.append((CPUInstruction.CONSUME, -1))
            self.instructions.append((CPUInstruction.GOTO, 0))
            Process.consumer_num += 1
            self.process_name = "Consumer_" + str(Process.consumer_num)
        self.instructions_num = len(self.instructions)

