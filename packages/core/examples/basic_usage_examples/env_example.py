import modi_plus
import time

"""
Example script for the usage of env module
Make sure you connect 1 env module to your network module
"""

if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()
    env = bundle.envs[0]

    while True:
        print(f"humidity(%): {env.humidity:<10} temperature(°C): {env.temperature:<10} "
              f"illuminance(%): {env.illuminance:<10} Volume(%): {env.volume:<10}", end="\r")
        time.sleep(0.02)
