"""Example: RGB Color Detection with multiple Env modules

This example demonstrates color detection using RGB sensors.
Works with multiple Env modules simultaneously.
"""

import modi_plus
import time


def detect_color(r, g, b, threshold=50):
    """Detect dominant color from RGB values

    Args:
        r, g, b: RGB values (0-255)
        threshold: Minimum difference to consider dominant

    Returns:
        Color name string
    """
    # Calculate relative differences
    colors = {'R': r, 'G': g, 'B': b}
    max_color = max(colors, key=colors.get)
    max_value = colors[max_color]

    # Check if dominant enough
    other_values = [v for k, v in colors.items() if k != max_color]
    if max_value - max(other_values) < threshold:
        return "MIXED/GRAY"

    # Determine color
    if max_color == 'R':
        if g > 100 and b < 50:
            return "YELLOW"
        elif g < 50 and b < 50:
            return "RED"
        elif g > 100 and b > 100:
            return "WHITE"
    elif max_color == 'G':
        if r < 50 and b < 50:
            return "GREEN"
        elif r > 100 and b > 100:
            return "WHITE"
    elif max_color == 'B':
        if r < 50 and g < 50:
            return "BLUE"
        elif r > 100 and g < 50:
            return "PURPLE"
        elif r > 100 and g > 100:
            return "WHITE"

    return "MIXED"


def get_rgb_modules(bundle):
    """Get all RGB-capable Env modules"""
    rgb_modules = []
    for i, env in enumerate(bundle.envs):
        if hasattr(env, '_is_rgb_supported') and env._is_rgb_supported():
            rgb_modules.append({
                'index': i,
                'env': env,
                'id': env.id,
                'version': env.app_version
            })
    return rgb_modules


def color_detection_demo(rgb_modules):
    """Run color detection on all RGB modules"""
    print(f"\n{'=' * 70}")
    print(f"Color Detection - {len(rgb_modules)} RGB Sensor(s)")
    print("Press Ctrl+C to stop")
    print(f"{'=' * 70}\n")

    try:
        while True:
            output_lines = []

            for m in rgb_modules:
                try:
                    m['env'].set_rgb_mode(m['env'].RGB_MODE_DUALSHOT)
                    # m['env'].set_rgb_mode(m['env'].RGB_MODE_ON)
                      # Ensure RGB mode is enabled
                    r, g, b = m['env'].rgb
                    color = detect_color(r, g, b)

                    # Create color bar (simple ASCII visualization)
                    r_bar = '█' * (r // 10)
                    g_bar = '█' * (g // 10)
                    b_bar = '█' * (b // 10)

                    output_lines.append(
                        f"Module #{m['index'] + 1} (0x{m['id']:X}): "
                        f"RGB=({r:3d}, {g:3d}, {b:3d}) -> {color:12s}"
                    )
                    output_lines.append(f"  R: {r_bar}")
                    output_lines.append(f"  G: {g_bar}")
                    output_lines.append(f"  B: {b_bar}")
                    output_lines.append("")

                except Exception as e:
                    output_lines.append(f"Module #{m['index'] + 1}: Error - {e}\n")

            # Clear and display
            print("\033[2J\033[H", end="")  # Clear screen
            print(f"{'=' * 70}")
            print("RGB Color Detection Monitor")
            print(f"{'=' * 70}\n")
            for line in output_lines:
                print(line)

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n\nStopped by user")


if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()

    print("=" * 70)
    print("RGB Color Detection Example")
    print("=" * 70)

    # Find RGB-capable modules
    print(f"\nScanning for RGB-capable Env modules...")
    rgb_modules = get_rgb_modules(bundle)

    if not rgb_modules:
        print("\nError: No RGB-capable Env modules found!")
        print("This example requires Env module version 2.x or higher")
        bundle.close()
        exit(1)

    print(f"Found {len(rgb_modules)} RGB-capable module(s):")
    for m in rgb_modules:
        print(f"  Module #{m['index'] + 1}: ID=0x{m['id']:X}, Version={m['version']}")

    # Start color detection
    input("\nPress Enter to start color detection...")
    color_detection_demo(rgb_modules)

    bundle.close()
