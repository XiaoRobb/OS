class Controller:
    def __init__(self):
        self.bitmap = [[] for _ in range(8)]
        for x in self.bitmap:
            for _ in range(8):
                x.append(0)
        self.files = {}

    def print_bitmap(self):
        for x in self.bitmap:
            for y in x:
                print(str(y)+"\t", end="")
            print()

    def print_files(self):
        for key in self.files:
            print("*********************************")
            print("文件"+key+"的物理空间如下：")
            for i, j in self.files[key]:
                Controller.get_real_position(i, j)

    def start(self):
        while True:
            print("****************************************************************************************************")
            print("您可以输入in来申请磁盘，输入out来释放，输入look来查看磁盘情况，输入files来查看文件的情况！！,输入end结束")
            flag = input("输入：")
            if flag == "in":
                name = input("输入文件名称：")
                zoom = int(input("输入想要申请空间的大小:"))
                if self.files.__contains__(name):
                    print("已有名为："+name+"的文件了！")
                elif zoom > self.get_left_zoom():
                    print("没有这么多空间了！")
                else:
                    self.files[name] = self.apply(zoom)
                    print("申请文件所存放的位置如下：")
                    for i, j in self.files[name]:
                        Controller.get_real_position(i, j)
            elif flag == "out":
                name = input("输入想要删除文件的名称：")
                if self.remove(name):
                    print("删除成功！")
                else:
                    print("此文件不存在！")
            elif flag == "look":
                self.print_bitmap()
            elif flag == "files":
                self.print_files()
            elif flag == "end":
                print("退出！！")
                break
            else:
                print("命令错误，请重新输入！！")

    @staticmethod
    def get_real_position(i, j):
        print("柱面号：" + str(i) + "磁道号：" + str(j // 4) + "物理记录号：" + str(j % 4))

    def get_left_zoom(self):
        left_zoom = 0
        for x in self.bitmap:
            for y in x:
                if y == 0:
                    left_zoom += 1
        return left_zoom

    def apply(self, zoom):
        positions = []
        for i, x in enumerate(self.bitmap):
            for j, y in enumerate(x):
                if y == 0:
                    self.bitmap[i][j] = 1
                    positions.append((i, j))
                    zoom -= 1
                if zoom <= 0:
                    break
            if zoom <= 0:
                break
        return positions

    def remove(self, name):
        if self.files.__contains__(name):
            print("文件："+name+"的各个块对应于位示图中位置如下：")
            for i, j in self.files[name]:
                self.bitmap[i][j] = 0
                print("字节号：" + str(i) + "\t位数" + str(j))
            self.files.pop(name)
            return True
        else:
            return False

