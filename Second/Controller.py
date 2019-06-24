from Second import PCB


class Controller:
    def __init__(self):
        self.max_size = 128
        self.table = [[0, self.max_size]]
        self.pcbs = []

    def start(self):
        print("实验开始！")
        while True:
            print("您可以输入in来申请主存，输入out来释放，输入look来查看主存情况！！,输入end结束")
            flag = input("输入：")
            if flag == "in":
                zoom = int(input("请输入申请进程的大小："))
                if self.apply(zoom):
                    print("申请成功！！")
                else:
                    print("空间不足！！，请重试！！")
            elif flag == "out":
                pcd_id = int(input("请输入释放进程的id："))
                if self.remove(pcd_id):
                    print("删除成功！")
                else:
                    print("没有id为："+pcd_id+"的进程！")
            elif flag == "look":
                self.look()
            elif flag == "end":
                print("退出！！")
                break
            else:
                print("命令错误，请重新输入！！")

    def apply(self, zoom):
        if zoom > self.max_size:
            return False
        else:
            for i, rest in enumerate(self.table):
                if rest[1] >= zoom:
                    pcb = PCB.PCB(zoom)
                    self.pcbs.append([rest[0], pcb])
                    length = rest[1] - zoom
                    if length > 0:
                        self.table[i] = [rest[0] + zoom, length]
                    else:
                        self.table.pop(i)
                    return True
            return False

    def remove(self, pcb_id):
        index = self.find(pcb_id)
        if index >= 0:
            pcb = self.pcbs[index]
            flag = True
            for i, rest in enumerate(self.table):
                if pcb[0] == rest[0] + rest[1]:
                    self.table[i] = [rest[0], rest[1]+pcb[1].zoom]
                    if i < len(self.table) and pcb[0] + pcb[1].zoom == self.table[i+1][0]:
                        self.table[i] = [rest[0], self.table[i][1] + self.table[i+1][1]]
                    self.table.pop(i+1)
                    flag = False
                    break
                if pcb[0] + pcb[1].zoom == rest[0]:
                    self.table[i] = [pcb[0], rest[1] + pcb[1].zoom]
                    flag = False
                    break
            if flag:
                self.table.append([pcb[0], pcb[1].zoom])
                self.table = sorted(self.table, key=lambda xx: xx[0])
            self.pcbs.pop(index)
            return True
        else:
            return False

    def look(self):
        print("************************运行进程显示*********************")
        for pcb in self.pcbs:
            print("进程："+str(pcb[1].id)+"\t所在起始地址为：Ox"+str(pcb[0])+"\t大小为:"+str(pcb[1].zoom))
        print("************************空闲分区显示*********************")
        for i, rest in enumerate(self.table):
            print("分区号："+str(i)+"\t所在起始地址为：Ox"+str(rest[0])+"\t长度为:"+str(rest[1]))

    def find(self, pcb_id):
        for i, pcb in enumerate(self.pcbs):
            if pcb_id == pcb[1].id:
                return i
        else:
            return -1






