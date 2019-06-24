import xml.dom.minidom
from First import PCB


def parse_xml():
    # 使用minidom解析器打开XML文档
    dom_tree = xml.dom.minidom.parse("data.xml")
    root = dom_tree.documentElement
    pcbs = root.getElementsByTagName("PCB")
    mypcbs = []
    for pcb in pcbs:
        name = pcb.getAttribute("name")
        estimate_time = int(pcb.getElementsByTagName("estimate_time")[0].childNodes[0].data)
        priority = int(pcb.getElementsByTagName("priority")[0].childNodes[0].data)
        mypcbs.append(PCB.PCB(name, estimate_time, priority))
    return mypcbs

