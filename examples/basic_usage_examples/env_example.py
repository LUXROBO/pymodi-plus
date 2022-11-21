import modi_plus

"""
Example script for the usage of env module
Make sure you connect 1 env module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    env = bundle.envs[0]

    while True:
        print("humidity: {0:<10} temp: {1:<10} "
              "intensity: {2:<10} Volume: {3:<10}".format(env.humidity,
                                                          env.temperature,
                                                          env.intensity,
                                                          env.volume), end="\r")
