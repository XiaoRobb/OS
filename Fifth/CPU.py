
from Fifth.Global import CPUInstruction
from Fifth.Global import Glo
from Fifth.Global import Semaphore
from Fifth import PCB
import random


class CPU:

    @staticmethod
    def run(process_with_pcb):
        Glo.pc = process_with_pcb.pcb.breakpoint
        while process_with_pcb.pcb.state == PCB.PCBState.Running:
            CPU.exe_instruction(process_with_pcb)
        return process_with_pcb.pcb.state

    @staticmethod
    def exe_instruction(process_with_pcb):
        process = process_with_pcb.process
        pcb = process_with_pcb.pcb
        Glo.pc += 1
        cpu_instruction = process.instructions[Glo.pc][0]
        if cpu_instruction == CPUInstruction.P:
            CPU.exe_p(process.instructions[Glo.pc][1], pcb, process)
        elif cpu_instruction == CPUInstruction.V:
            CPU.exe_v(process.instructions[Glo.pc][1], pcb, process)
        elif cpu_instruction == CPUInstruction.PUT:
            CPU.exe_put(process)
            CPU.change_state(pcb)
        elif cpu_instruction == CPUInstruction.GET:
            CPU.exe_get(process)
            CPU.change_state(pcb)
        elif cpu_instruction == CPUInstruction.PRODUCE:
            CPU.exe_produce(process)
            CPU.change_state(pcb)
        elif cpu_instruction == CPUInstruction.CONSUME:
            CPU.exe_consume(process)
            CPU.change_state(pcb)
        else:
            CPU.exe_goto(pcb, process)
            if pcb.state != PCB.PCBState.End:
                CPU.change_state(pcb)

    @staticmethod
    def change_state(pcb):
        pcb.state = PCB.PCBState.Runable
        pcb.reason = PCB.PCBWaitingReason.ReasonN
        pcb.breakpoint = Glo.pc

    @staticmethod
    def exe_p(semaphore, pcb, process):
        if semaphore == Semaphore.Empty:

            Glo.empty -= 1
            if Glo.empty < 0:
                # W(empty)
                print(process.print_holder+process.process_name + ":执行P处理指令P（Empty),但缓冲区已满，进入等待状态")
                pcb.state = PCB.PCBState.Waiting
                pcb.reason = PCB.PCBWaitingReason.ReasonEmpty
                pcb.breakpoint = Glo.pc
            else:
                print(process.print_holder+process.process_name + ":执行P处理指令P（Empty)")
                CPU.change_state(pcb)
        else:
            Glo.full -= 1
            if Glo.full < 0:
                # W(full)
                print(process.print_holder+process.process_name + ":执行P处理指令P（Full),但缓冲区没有产品，进入等待状态")
                pcb.state = PCB.PCBState.Waiting
                pcb.reason = PCB.PCBWaitingReason.ReasonFull
                pcb.breakpoint = Glo.pc
            else:
                print(process.print_holder + process.process_name + ":执行P处理指令P（Full)")
                CPU.change_state(pcb)

    @staticmethod
    def exe_v(semaphore, pcb, process):
        if semaphore == Semaphore.Empty:
            Glo.empty += 1
            if Glo.empty <= 0:
                # R(empty)
                print(process.print_holder+process.process_name + ":执行V处理指令V（Empty),唤醒一个Producer进程")
                Glo.wake_process_for_empty()
            else:
                print(process.print_holder + process.process_name + ":执行V处理指令V（Empty)")
        else:
            Glo.full += 1
            if Glo.full <= 0:
                # R(full)
                print(process.print_holder + process.process_name + ":执行V处理指令V（Full),唤醒一个Consumer进程")
                Glo.wake_process_for_full()
            else:
                print(process.print_holder + process.process_name + ":执行V处理指令V（Full)")
        CPU.change_state(pcb)

    @staticmethod
    def exe_put(process):
        Glo.products[Glo.products_in_pointer] = Glo.product_in
        Glo.products_in_pointer = (Glo.products_in_pointer + 1) % 10
        print(process.print_holder + process.process_name + ":执行PUT指令,将产品:" + Glo.product_in + "\t放入缓冲区")

    @staticmethod
    def exe_get(process):
        Glo.product_out = Glo.products[Glo.products_out_pointer]
        Glo.products_out_pointer = (Glo.products_out_pointer + 1) % 10
        print(process.print_holder + process.process_name + ":执行GET指令,从缓冲区中获得了一个产品："+Glo.product_out+"\t还未消耗")

    @staticmethod
    def exe_produce(process):
        index = random.randint(97, 122)
        Glo.product_in = chr(index)
        print(process.print_holder + process.process_name + ":执行PRODUCE指令,生产了一个产品:"+Glo.product_in+"\t还未放入缓冲区")

    @staticmethod
    def exe_consume(process):
        print(process.print_holder + process.process_name + ":执行CONSUME指令,消耗了一个产品:" + Glo.product_out)

    @staticmethod
    def exe_goto(pcb, process):

        # 此进程已经完整运行了一次生产了一个产品，判断是否还需要再生产
        process.run_times -= 1
        if process.run_times == 0:
            pcb.state = PCB.PCBState.End
            print(process.print_holder + process.process_name + ":执行GOTO指令,进程全部完成，进入结束状态！！")
        else:
            print(process.print_holder + process.process_name + ":执行GOTO指令,回到开始重新生产")
        Glo.pc = -1




