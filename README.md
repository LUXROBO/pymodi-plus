<div align="center">

[![Python Versions](https://img.shields.io/pypi/pyversions/pymodi-plus.svg?style=flat-square)](https://pypi.python.org/pypi/pymodi-plus)
[![PyPI Release (latest by date)](https://img.shields.io/github/v/release/LUXROBO/pymodi-plus?style=flat-square)](https://pypi.python.org/pypi/pymodi-plus)
[![Read the Docs (version)](https://img.shields.io/readthedocs/pymodi-plus/latest?style=flat-square)](https://pymodi-plus.readthedocs.io/en/latest/?badge=master)
[![GitHub Workflow Status (Build)](https://img.shields.io/github/actions/workflow/status/LUXROBO/pymodi-plus/build.yml?branch=master)](https://github.com/LUXROBO/pymodi-plus/actions)
[![GitHub LICENSE](https://img.shields.io/github/license/LUXROBO/pymodi-plus?style=flat-square&color=blue)](https://github.com/LUXROBO/pymodi-plus/blob/master/LICENSE)

</div>

# PyMODI+ Monorepo

> Python API for controlling modular electronics, MODI+ - Desktop and Web support

This monorepo contains two packages:

| Package | Description | PyPI |
|---------|-------------|------|
| **[packages/core](./packages/core/)** | Core library for desktop (USB/BLE) | `pymodi-plus` |
| **[packages/web](./packages/web/)** | Web extension for Pyodide/Browser | `pymodi-plus-web` |

## Quick Start

### Desktop Usage (USB/BLE)

```bash
# Install with all features
pip install pymodi-plus[all]

# Or minimal install
pip install pymodi-plus
```

```python
import modi_plus

bundle = modi_plus.MODIPlus()
led = bundle.leds[0]
led.turn_on()
```

### Web/Pyodide Usage

```python
# In Pyodide environment
import micropip
await micropip.install('pymodi-plus-web')

from modi_plus_web import MODIPlusWeb

modi = MODIPlusWeb()
modi.set_send_callback(js_send_function)
# ... use like regular MODIPlus
```

## Development

```bash
# Install all packages in development mode
make install-all

# Run all tests
make test-monorepo

# Build all packages
make build-all
```

### Package-specific commands

```bash
# Core package
make install-core
make test-core
make build-core

# Web package
make install-web
make test-web
make build-web
```

## Architecture

```
pymodi-plus/
├── packages/
│   ├── core/           # pymodi-plus (PyPI)
│   │   ├── modi_plus/  # Core library
│   │   ├── tests/
│   │   └── setup.py
│   └── web/            # pymodi-plus-web (PyPI)
│       ├── modi_plus_web/
│       ├── tests/
│       └── setup.py
├── docs/               # Documentation
├── Makefile           # Monorepo commands
└── pyproject.toml     # Root configuration
```

## Documentation

- [Quick Start Guide](./docs/getting-started/QUICKSTART.md)
- [Env Module RGB Features](./docs/features/ENV_RGB_FEATURE.md)
- [Development Guide](./docs/development/MAKEFILE_GUIDE.md)
- [Web Package README](./packages/web/README.md)

## Contributing

We welcome contributions! Please see:
- [Contributing Guidelines](./docs/getting-started/CONTRIBUTING.md)
- [Code of Conduct](./docs/getting-started/CODE_OF_CONDUCT.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
