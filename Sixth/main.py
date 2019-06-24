from Sixth.PCB import PCB
from Sixth.PCB import PCBState
from Sixth.Process import Process
from Sixth.Process import ProcessType
from Sixth.ProcessWithPCB import ProcessWithPCB
from Sixth.CPU import CPU
from Sixth.Global import Glo
import random


def main():

    producer_num = int(input("请设置生产者数量："))
    producer_times = []
    for i in range(producer_num):
        x = input("请设置Producer"+str(i)+"的生产数量：")
        producer_times.append(int(x))
    consumer_num = int(input("请设置消费者数量："))
    # 初始化producer_num个生成者进程,并生成对应的进程控制块PCB，并将两者打包,并将其加入就绪队列
    for i in range(producer_num):
        process = Process(ProcessType.Producer, producer_times[i])
        pcb = PCB()
        process_with_pcb = ProcessWithPCB(process, pcb)
        Glo.process_with_pcbs.append(process_with_pcb)
        Glo.runable_processes.append(process_with_pcb)

    # 初始化consumer_num个消费者进程,并生成对应的进程控制块PCB，并将两者打包,并将其加入就绪队列
    for i in range(consumer_num):
        process = Process(ProcessType.Consumer, 999)
        pcb = PCB()
        process_with_pcb = ProcessWithPCB(process, pcb)
        Glo.process_with_pcbs.append(process_with_pcb)
        Glo.runable_processes.append(process_with_pcb)

    while len(Glo.runable_processes) > 0:
        if Glo.running_process is None:
            index = random.randint(0, len(Glo.runable_processes) - 1)
            Glo.running_process = Glo.runable_processes[index]
            Glo.running_process.pcb.state = PCBState.Running
            Glo.runable_processes.pop(index)
            print("\n\n")
            print("****************进程:" + Glo.running_process.process.process_name + "开始进入CPU执行****************")
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
