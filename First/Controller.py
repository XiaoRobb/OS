import time


class Controller:
    def __init__(self, pcbs):
        self.runable = pcbs
        self.runable = sorted(self.runable, key=lambda pcb: pcb.__getattribute__("priority"), reverse=True)
        self.ends = []
        self.ranning = None

    def start(self):
        while True:
            if self.ranning is None:
                if self.runable:
                    print("*******************************************")
                    self.ranning = self.runable[0]
                    self.runable.pop(0)
                    print("将就绪队列的队首进程:"+self.ranning.name+"出队，进入运行态")
                    print(self.ranning.name+"正在运行......")
                    print("如下进程正在就绪队列:")
                    for pbc in self.runable:
                        print("\t"+pbc.name+"(优先级:"+str(pbc.priority)+")"+"剩余要求运行时间:"+str(pbc.estimate_time))
                    time.sleep(1)
                    print(self.ranning.name + "此次运行结束")
                    self.ranning.estimate_time -= 1
                    self.ranning.priority -= 1
                    if self.ranning.estimate_time > 0:
                        print("进程:" + self.ranning.name + "进入就绪队列")
                        self.runable.append(self.ranning)
                        self.runable = sorted(self.runable, key=lambda pcb: pcb.__getattribute__("priority"),
                                              reverse=True)
                        print("如下进程正在就绪队列:")
                        for pbc in self.runable:
                            print("\t" + pbc.name + "(优先级:" + str(pbc.priority) + ")" + "剩余要求运行时间:" + str(
                                pbc.estimate_time))
                        self.ranning = None
                    else:
                        self.ranning.estimate_time = 0
                        print("进程:"+self.ranning.name + "全部运行结束")
                        self.ends.append(self.ranning)
                        self.ranning = None
                else:
                    print("*******************************************")
                    print("所有进程运行完毕！！")
                    break





