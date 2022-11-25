import modi_plus

"""
Example script for the usage of env module
Make sure you connect 1 env module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    env = bundle.envs[0]

    while True:
        print(f"humidity(%): {env.humidity:<10} temperature(°C): {env.temperature:<10} "
              f"intensity(%): {env.intensity:<10} Volume(%): {env.volume:<10}", end="\r")
