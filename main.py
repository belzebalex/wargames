from simulation import DarwinSelection
from display import Display
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sel = DarwinSelection()
        sel.run()

    elif sys.argv[1] == "-display":
        dis = Display()
        dis.run()
