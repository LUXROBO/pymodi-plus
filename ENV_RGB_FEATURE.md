# Env Module RGB Feature Documentation

## Overview

The Environment (Env) module now supports RGB color sensor properties starting from **app version 2.x**. This feature allows you to read Red, Green, and Blue color values from the environment sensor.

## Version Compatibility

| Version | RGB Support | Properties Available |
|---------|-------------|---------------------|
| 1.x | ❌ Not Supported | Temperature, Humidity, Illuminance, Volume |
| 2.x | ✅ Supported | Temperature, Humidity, Illuminance, Volume, **Red, Green, Blue** |
| 3.x+ | ✅ Supported | Temperature, Humidity, Illuminance, Volume, **Red, Green, Blue** |

## Property Offsets

```python
PROPERTY_OFFSET_ILLUMINANCE = 0   # Bytes 0-1
PROPERTY_OFFSET_TEMPERATURE = 2   # Bytes 2-3
PROPERTY_OFFSET_HUMIDITY = 4      # Bytes 4-5
PROPERTY_OFFSET_VOLUME = 6        # Bytes 6-7
PROPERTY_OFFSET_RED = 8           # Bytes 8-9  (Version 2.x+)
PROPERTY_OFFSET_GREEN = 10        # Bytes 10-11 (Version 2.x+)
PROPERTY_OFFSET_BLUE = 12         # Bytes 12-13 (Version 2.x+)
```

## API Reference

### Properties

#### `env.red` (Version 2.x+ only)
Returns the red color value between 0 and 255.

**Returns:** `int`

**Raises:** `AttributeError` if app version is 1.x

**Example:**
```python
red_value = env.red
print(f"Red: {red_value}")
```

---

#### `env.green` (Version 2.x+ only)
Returns the green color value between 0 and 255.

**Returns:** `int`

**Raises:** `AttributeError` if app version is 1.x

**Example:**
```python
green_value = env.green
print(f"Green: {green_value}")
```

---

#### `env.blue` (Version 2.x+ only)
Returns the blue color value between 0 and 255.

**Returns:** `int`

**Raises:** `AttributeError` if app version is 1.x

**Example:**
```python
blue_value = env.blue
print(f"Blue: {blue_value}")
```

---

#### `env.rgb` (Version 2.x+ only)
Returns all RGB color values as a tuple.

**Returns:** `tuple` - (red, green, blue)

**Raises:** `AttributeError` if app version is 1.x

**Example:**
```python
r, g, b = env.rgb
print(f"RGB: ({r}, {g}, {b})")
```

---

### Methods

#### `env._is_rgb_supported()`
Check if RGB properties are supported based on app version.

**Returns:** `bool` - True if RGB is supported, False otherwise

**Example:**
```python
if env._is_rgb_supported():
    print("RGB is supported!")
    rgb = env.rgb
else:
    print("RGB is not supported in this version")
```

## Usage Examples

### Example 1: Basic RGB Reading (Version 2.x+)

```python
import modi_plus

bundle = modi_plus.MODI()
env = bundle.envs[0]

# Read individual RGB values
red = env.red
green = env.green
blue = env.blue

print(f"Red: {red}, Green: {green}, Blue: {blue}")

bundle.close()
```

### Example 2: Using RGB Tuple (Version 2.x+)

```python
import modi_plus

bundle = modi_plus.MODI()
env = bundle.envs[0]

# Read all RGB values at once
r, g, b = env.rgb
print(f"RGB: ({r}, {g}, {b})")

bundle.close()
```

### Example 3: Version-Safe RGB Access

```python
import modi_plus

bundle = modi_plus.MODI()
env = bundle.envs[0]

print(f"App Version: {env.app_version}")

# Check version before accessing RGB
if env._is_rgb_supported():
    print("RGB Color Sensor:")
    r, g, b = env.rgb
    print(f"  Red:   {r}")
    print(f"  Green: {g}")
    print(f"  Blue:  {b}")
else:
    print("RGB not supported in this version")
    print("Available sensors:")
    print(f"  Temperature: {env.temperature}°C")
    print(f"  Humidity: {env.humidity}%")

bundle.close()
```

### Example 4: Color Detection

```python
import modi_plus
import time

bundle = modi_plus.MODI()
env = bundle.envs[0]

if not env._is_rgb_supported():
    print("Error: RGB is not supported")
    exit(1)

print("Color Detection (Press Ctrl+C to stop)")

try:
    while True:
        r, g, b = env.rgb

        # Determine dominant color
        if r > g and r > b:
            color = "RED"
        elif g > r and g > b:
            color = "GREEN"
        elif b > r and b > g:
            color = "BLUE"
        else:
            color = "MIXED"

        print(f"\rRGB: ({r:3d}, {g:3d}, {b:3d}) - {color}  ", end="", flush=True)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopped")

bundle.close()
```

## Error Handling

### Version 1.x - RGB Not Supported

If you try to access RGB properties on version 1.x, you'll get an `AttributeError`:

```python
import modi_plus

bundle = modi_plus.MODI()
env = bundle.envs[0]  # App version 1.5.0

try:
    red = env.red
except AttributeError as e:
    print(f"Error: {e}")
    # Output: RGB properties are not supported in Env module version 1.x.
    #         Please upgrade to version 2.x or above.
```

### Safe Access Pattern

Always check version support before accessing RGB:

```python
import modi_plus

bundle = modi_plus.MODI()
env = bundle.envs[0]

if env._is_rgb_supported():
    # Safe to use RGB
    rgb = env.rgb
    print(f"RGB: {rgb}")
else:
    # Use alternative sensors
    print(f"Illuminance: {env.illuminance}")
```

## Testing

Comprehensive tests are available for RGB functionality:

```bash
# Run all Env module tests (including RGB)
python3 -m pytest tests/module/input_module/test_env.py -v

# Run only RGB-related tests
python3 -m pytest tests/module/input_module/test_env.py::TestEnvRGBVersion2 -v
```

### Test Coverage

- ✅ RGB properties in version 1.x (should raise AttributeError)
- ✅ RGB properties in version 2.x (should work)
- ✅ RGB properties in version 3.x (should work)
- ✅ RGB properties without version set (should raise AttributeError)
- ✅ Individual color properties (red, green, blue)
- ✅ RGB tuple property
- ✅ Version support check method
- ✅ Property offset validation

**Total RGB tests:** 15 test cases

**Test Results:**
```bash
$ python3 -m pytest tests/module/input_module/test_env.py -v
============================== 19 passed in 0.03s ==============================
```

## Implementation Details

### Version Format

App version is encoded as a 16-bit integer:
```
version = (major << 13) | (minor << 8) | patch

Examples:
- 1.5.0 = (1 << 13) | (5 << 8) | 0 = 9472
- 2.0.0 = (2 << 13) | (0 << 8) | 0 = 16384
- 3.2.1 = (3 << 13) | (2 << 8) | 1 = 25089
```

### RGB Support Check

```python
def _is_rgb_supported(self) -> bool:
    if not hasattr(self, '_Module__app_version') or self._Module__app_version is None:
        return False

    # Extract major version
    major_version = self._Module__app_version >> 13
    return major_version >= 2
```

## Migration Guide

### Upgrading from Version 1.x to 2.x

If your code uses version 1.x Env modules and you upgrade to version 2.x:

**Before (Version 1.x compatible):**
```python
env = bundle.envs[0]
temp = env.temperature
humidity = env.humidity
```

**After (Version 2.x with RGB):**
```python
env = bundle.envs[0]

# Old properties still work
temp = env.temperature
humidity = env.humidity

# New RGB properties available
if env._is_rgb_supported():
    r, g, b = env.rgb
    print(f"RGB: ({r}, {g}, {b})")
```

### Backward Compatibility

The implementation is **fully backward compatible**:
- Version 1.x modules work without any code changes
- New RGB properties only work on version 2.x+
- Version check prevents errors on older modules

## Troubleshooting

### Issue: AttributeError when accessing RGB

**Cause:** Env module app version is 1.x

**Solution:**
1. Check module version: `print(env.app_version)`
2. Upgrade firmware to version 2.x or above
3. Or add version check in code:
   ```python
   if env._is_rgb_supported():
       rgb = env.rgb
   ```

### Issue: RGB values always 0

**Possible causes:**
1. Sensor is in a dark environment
2. Sensor calibration needed
3. Check if sensor is covered

**Solution:**
- Point sensor at colored object
- Ensure good lighting
- Check sensor is not obstructed

## Summary

| Feature | Details |
|---------|---------|
| **Minimum Version** | 2.0.0 |
| **New Properties** | `red`, `green`, `blue`, `rgb` |
| **Value Range** | 0-255 for each color |
| **Backward Compatible** | ✅ Yes |
| **Test Coverage** | 15 test cases |
| **Example Code** | `examples/basic_usage_examples/env_rgb_example.py` |

For more information, see the [test file](tests/module/input_module/test_env.py) for detailed usage examples.
