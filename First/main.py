from First import Controller
from First import DataReader


def main():
    controller = Controller.Controller(DataReader.parse_xml())
    controller.start()


if __name__ == "__main__":
    main()
