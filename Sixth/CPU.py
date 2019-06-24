
from Sixth.Global import CPUInstruction
from Sixth.Global import Glo
from Sixth.Global import Semaphore
from Sixth import PCB
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
            CPU.exe_p(process.instructions[Glo.pc][1], pcb)
        elif cpu_instruction == CPUInstruction.V:
            CPU.exe_v(process.instructions[Glo.pc][1], pcb)
        elif cpu_instruction == CPUInstruction.PUT:
            CPU.exe_put(process.process_name)
            CPU.change_state(pcb)
        elif cpu_instruction == CPUInstruction.GET:
            CPU.exe_get(process.process_name)
            CPU.change_state(pcb)
        elif cpu_instruction == CPUInstruction.PRODUCE:
            CPU.exe_produce(process.process_name)
            CPU.change_state(pcb)
        elif cpu_instruction == CPUInstruction.CONSUME:
            CPU.exe_consume(process.process_name)
            CPU.change_state(pcb)
        else:
            CPU.exe_goto(process_with_pcb)
            if pcb.state != PCB.PCBState.End:
                CPU.change_state(pcb)

    @staticmethod
    def change_state(pcb):
        pcb.state = PCB.PCBState.Runable
        pcb.reason = PCB.PCBWaitingReason.ReasonN
        pcb.breakpoint = Glo.pc

    @staticmethod
    def exe_p(semaphore, pcb):
        if semaphore == Semaphore.Empty:
            print("执行P处理指令P（Empty)")
            Glo.empty -= 1
            if Glo.empty < 0:
                # W(empty)
                print("缓冲区已满，进入等待状态")
                pcb.state = PCB.PCBState.Waiting
                pcb.reason = PCB.PCBWaitingReason.ReasonEmpty
                pcb.breakpoint = Glo.pc
            else:
                CPU.change_state(pcb)
        else:
            print("执行P处理指令P（Full)")
            Glo.full -= 1
            if Glo.full < 0:
                # W(full)
                print("缓冲区没有产品，进入等待状态")
                pcb.state = PCB.PCBState.Waiting
                pcb.reason = PCB.PCBWaitingReason.ReasonFull
                pcb.breakpoint = Glo.pc
            else:
                CPU.change_state(pcb)

    @staticmethod
    def exe_v(semaphore, pcb):
        if semaphore == Semaphore.Empty:
            print("执行V处理指令V（Empty)")
            Glo.empty += 1
            if Glo.empty <= 0:
                # R(empty)
                print("唤醒一个Producer进程")
                Glo.wake_process_for_empty()
        else:
            print("执行V处理指令V（Full)")
            Glo.full += 1
            if Glo.full <= 0:
                # R(full)
                print("唤醒一个Consumer进程")
                Glo.wake_process_for_full()
        CPU.change_state(pcb)

    @staticmethod
    def exe_put(process_name):
        Glo.products[Glo.products_in_pointer] = Glo.product_in[process_name]
        Glo.products_in_pointer = (Glo.products_in_pointer + 1) % 10
        print("执行PUT指令,将产品:" + Glo.product_in[process_name] + "\t放入缓冲区")

    @staticmethod
    def exe_get(process_name):
        Glo.product_out[process_name] = Glo.products[Glo.products_out_pointer]
        Glo.products_out_pointer = (Glo.products_out_pointer + 1) % 10
        print("执行GET指令,从缓冲区中获得了一个产品："+Glo.product_out[process_name]+"\t还未消耗")

    @staticmethod
    def exe_produce(process_name):
        index = random.randint(97, 122)
        Glo.product_in[process_name] = chr(index)
        print("执行PRODUCE指令,生产了一个产品:"+Glo.product_in[process_name]+"\t还未放入缓冲区")

    @staticmethod
    def exe_consume(process_name):
        print("执行CONSUME指令,消耗了一个产品:" + Glo.product_out[process_name])

    @staticmethod
    def exe_goto(process_with_pcb):
        print("执行GOTO指令")
        # 此进程已经完整运行了一次生产了一个产品，判断是否还需要再生产
        process_with_pcb.process.run_times -= 1
        if process_with_pcb.process.run_times == 0:
            process_with_pcb.pcb.state = PCB.PCBState.End
            print("进程："+process_with_pcb.process.process_name+"完成！")
        Glo.pc = -1




