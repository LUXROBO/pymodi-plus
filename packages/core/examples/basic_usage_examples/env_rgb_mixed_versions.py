"""Example: Mixed version Env modules (v1.x and v2.x together)

This example shows how to handle multiple Env modules with different versions.
Some modules may support RGB (v2.x+) while others don't (v1.x).
"""

import modi_plus
import time


def classify_env_modules(envs):
    """Classify Env modules by RGB support"""
    rgb_modules = []
    legacy_modules = []

    for i, env in enumerate(envs):
        module_info = {
            'index': i,
            'env': env,
            'id': env.id,
            'version': env.app_version
        }

        if hasattr(env, '_is_rgb_supported') and env._is_rgb_supported():
            rgb_modules.append(module_info)
        else:
            legacy_modules.append(module_info)

    return rgb_modules, legacy_modules


def print_module_summary(rgb_modules, legacy_modules):
    """Print summary of all connected modules"""
    total = len(rgb_modules) + len(legacy_modules)

    print(f"\n{'=' * 70}")
    print(f"Connected Env Modules Summary ({total} total)")
    print(f"{'=' * 70}")

    if rgb_modules:
        print(f"\n✓ RGB-capable modules (v2.x+): {len(rgb_modules)}")
        for m in rgb_modules:
            print(f"  Module #{m['index'] + 1}: ID=0x{m['id']:X}, Version={m['version']}")

    if legacy_modules:
        print(f"\n✗ Legacy modules (v1.x): {len(legacy_modules)}")
        for m in legacy_modules:
            print(f"  Module #{m['index'] + 1}: ID=0x{m['id']:X}, Version={m['version']}")


def read_all_sensors(rgb_modules, legacy_modules):
    """Read all available sensors from all modules"""
    print(f"\n{'=' * 70}")
    print("Reading sensor values from all modules (Press Ctrl+C to stop)")
    print(f"{'=' * 70}\n")

    try:
        while True:
            output_lines = []

            # Read RGB from v2.x modules
            if rgb_modules:
                output_lines.append("RGB Modules:")
                for m in rgb_modules:
                    try:
                        r, g, b = m['env'].rgb
                        temp = m['env'].temperature
                        output_lines.append(
                            f"  #{m['index'] + 1}: RGB=({r:3d},{g:3d},{b:3d}) "
                            f"Temp={temp:2d}°C"
                        )
                    except Exception as e:
                        output_lines.append(f"  #{m['index'] + 1}: Error - {e}")

            # Read sensors from v1.x modules
            if legacy_modules:
                output_lines.append("\nLegacy Modules:")
                for m in legacy_modules:
                    try:
                        temp = m['env'].temperature
                        hum = m['env'].humidity
                        lux = m['env'].illuminance
                        output_lines.append(
                            f"  #{m['index'] + 1}: Temp={temp:2d}°C "
                            f"Humidity={hum:2d}% Lux={lux:3d}"
                        )
                    except Exception as e:
                        output_lines.append(f"  #{m['index'] + 1}: Error - {e}")

            # Clear screen and print
            print("\033[2J\033[H", end="")  # Clear screen
            print(f"{'=' * 70}")
            print("Multi-Version Env Modules Monitor")
            print(f"{'=' * 70}")
            for line in output_lines:
                print(line)

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n\nStopped by user")


if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()

    print("=" * 70)
    print("Mixed Version Env Modules Example")
    print("=" * 70)

    # Check connected modules
    num_envs = len(bundle.envs)
    print(f"\nDetecting Env modules... Found {num_envs} module(s)")

    if num_envs == 0:
        print("Error: No Env modules found!")
        bundle.close()
        exit(1)

    # Classify by version
    rgb_modules, legacy_modules = classify_env_modules(bundle.envs)

    # Print summary
    print_module_summary(rgb_modules, legacy_modules)

    # Start reading
    if rgb_modules or legacy_modules:
        input("\nPress Enter to start monitoring...")
        read_all_sensors(rgb_modules, legacy_modules)
    else:
        print("\nNo modules found!")

    bundle.close()
