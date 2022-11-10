import modi_plus
import time

"""
Example script for the usage of button module
Make sure you connect 1 button module to your
network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()

    input()

    button0 = bundle.button(0x20307D218B0A)
    while True:
        print(f"pressed:{button0.pressed},\tclicked:{button0.clicked},\tdouble clicked:{button0.double_clicked},\ttoggled:{button0.toggled}      ", end="\r")
        time.sleep(0.02)
