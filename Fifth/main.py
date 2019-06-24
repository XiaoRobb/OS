from Fifth.PCB import PCB
from Fifth.PCB import PCBState
from Fifth.Process import Process
from Fifth.Process import ProcessType
from Fifth.ProcessWithPCB import ProcessWithPCB
from Fifth.CPU import CPU
from Fifth.Global import Glo
import random


def main():
    x = int(input("请设置Producer" + "的生产总数量："))
    process = Process(ProcessType.Producer, x)
    pcb = PCB()
    process_with_pcb = ProcessWithPCB(process, pcb)
    Glo.process_with_pcbs.append(process_with_pcb)
    Glo.runable_processes.append(process_with_pcb)

    process = Process(ProcessType.Consumer, 999)
    pcb = PCB()
    process_with_pcb = ProcessWithPCB(process, pcb)
    Glo.process_with_pcbs.append(process_with_pcb)
    Glo.runable_processes.append(process_with_pcb)

    print("\n\n")
    while len(Glo.runable_processes) > 0:
        if Glo.running_process is None:
            index = random.randint(0, len(Glo.runable_processes) - 1)
            Glo.running_process = Glo.runable_processes[index]
            Glo.running_process.pcb.state = PCBState.Running
            Glo.runable_processes.pop(index)
            state = CPU.run(Glo.running_process)
            if state == PCBState.Runable:
                Glo.runable_processes.append(Glo.running_process)
            elif state == PCBState.Waiting:
                if Glo.running_process.process.person_type == ProcessType.Producer:
                    Glo.waiting_processes_for_empty.append(Glo.running_process)
                else:
                    Glo.waiting_processes_for_full.append(Glo.running_process)
            elif state == PCBState.End:
                Glo.end_processes.append(Glo.end_processes)
            Glo.running_process = None
    print("\n\n")
    print("由于生产者已经结束，消费者一直在等待，所以我们自动结束了！！！！！")


if __name__ == "__main__":
    main()
