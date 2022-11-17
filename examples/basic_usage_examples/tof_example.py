import modi_plus

"""
Example script for the usage of tof module
Make sure you connect 1 tof module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    tof = bundle.tofs[0]

    while True:
        print("Distance: {0:<10}".format(tof.distance), end="\r")
