"""Example of using Env module RGB properties

This example demonstrates how to use the RGB color sensor properties
of the Env module. RGB properties are only available in version 2.x and above.

Note: This example tests ALL connected Env modules.
"""

import modi_plus
import time


def test_env_module(env, index):
    """Test a single Env module for RGB support"""
    print(f"\n{'=' * 60}")
    print(f"Env Module #{index + 1} (ID: 0x{env.id:X})")
    print(f"{'=' * 60}")
    print(f"App Version: {env.app_version}")

    # Check if version supports RGB
    if hasattr(env, '_is_rgb_supported') and env._is_rgb_supported():
        print("✓ RGB properties are supported!")
        return True
    else:
        print("✗ RGB properties are NOT supported in this version")
        print("Please upgrade firmware to version 2.x or above")
        print("\nAvailable properties:")
        print(f"  - Temperature: {env.temperature}°C")
        print(f"  - Humidity: {env.humidity}%")
        print(f"  - Illuminance: {env.illuminance} lux")
        print(f"  - Volume: {env.volume} dB")
        return False


if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()

    print("=" * 60)
    print("Env Module RGB Example - Multi-Module Support")
    print("=" * 60)

    # Check how many Env modules are connected
    num_envs = len(bundle.envs)
    print(f"\nFound {num_envs} Env module(s)")

    if num_envs == 0:
        print("Error: No Env modules found!")
        bundle.close()
        exit(1)

    # Test each Env module
    rgb_supported_modules = []
    for i, env in enumerate(bundle.envs):
        if test_env_module(env, i):
            rgb_supported_modules.append((i, env))

    # If any module supports RGB, start continuous reading
    if rgb_supported_modules:
        print(f"\n{'=' * 60}")
        print(f"Reading RGB values from {len(rgb_supported_modules)} module(s)")
        print("Press Ctrl+C to stop")
        print(f"{'=' * 60}\n")

        try:
            while True:
                # Read and display RGB from all supported modules
                for idx, env in rgb_supported_modules:
                    try:
                        r, g, b = env.rgb
                        print(f"Module #{idx + 1}: RGB=({r:3d}, {g:3d}, {b:3d})", end="  ")
                    except Exception as e:
                        print(f"Module #{idx + 1}: Error - {e}", end="  ")

                print("\r", end="", flush=True)
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n\nStopped by user")

    else:
        print(f"\n{'=' * 60}")
        print("No modules with RGB support found.")
        print("All connected modules are version 1.x")
        print(f"{'=' * 60}")

    bundle.close()
