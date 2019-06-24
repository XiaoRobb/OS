class PCB:
    num = 0

    def __init__(self, zoom):
        self.id = PCB.num
        PCB.num += 1
        self.zoom = zoom
