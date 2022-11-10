import modi
import time

"""
Example script for the usage of button module
Make sure you connect 1 button module to your
network module
"""

if __name__ == "__main__":
    bundle = modi.MODI()

    input()

    if len(bundle.buttons):
        button = bundle.buttons[0]
        while True:
            print(f"pressed:{button.pressed},\tclicked:{button.clicked},\tdouble clicked:{button.double_clicked},\ttoggled:{button.toggled}      ", end="\r")
            time.sleep(0.02)