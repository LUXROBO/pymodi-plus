# pymodi-plus-web

MODI+ Python Library for Web/Pyodide environments.

This package provides a `PostMessageTask` communication layer that enables `pymodi-plus` to work in web browsers via Pyodide, communicating with WebUSB through JavaScript postMessage.

## Installation

### In Pyodide (Browser)

```python
import micropip
await micropip.install('pymodi-plus-web')
```

### Local Development

```bash
pip install pymodi-plus-web
```

## Usage

### Basic Usage (Pyodide)

```python
from modi_plus_web import MODIPlusWeb

# Create MODI+ instance with postMessage communication
modi = MODIPlusWeb()

# Use standard MODI+ API
led = modi.led(0x1234)
led.rgb = (255, 0, 0)
```

### With JavaScript Integration

```javascript
// JavaScript side
const pyodide = await loadPyodide();
await pyodide.loadPackage('micropip');
await pyodide.runPythonAsync(`
    import micropip
    await micropip.install('pymodi-plus-web')

    from modi_plus_web import MODIPlusWeb
    modi = MODIPlusWeb()
`);

// Send data from WebUSB to Python
window.addEventListener('message', (e) => {
    if (e.data.type === 'modi_packet') {
        pyodide.runPython(`modi.task.on_message('${JSON.stringify(e.data.payload)}')`);
    }
});

// Set up Python to JavaScript callback
pyodide.runPython(`
    import js
    def send_to_webusb(pkt):
        js.parent.postMessage({'type': 'modi_packet', 'payload': pkt}, '*')
    modi.set_send_callback(send_to_webusb)
`);
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser                               │
│  ┌─────────────────┐      postMessage      ┌─────────────┐ │
│  │  modi_flutter   │ <──────────────────> │   iframe    │ │
│  │   (WebUSB)      │      JSON packets     │             │ │
│  │                 │                        │  ┌───────┐ │ │
│  │  MODI Hardware  │                        │  │Pyodide│ │ │
│  │  Connection     │                        │  │pymodi │ │ │
│  │                 │                        │  │-plus  │ │ │
│  └─────────────────┘                        │  │-web   │ │ │
│                                             │  └───────┘ │ │
│                                             └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## API Reference

### MODIPlusWeb

Inherits from `modi_plus.MODIPlus` with `PostMessageTask` as the default communication layer.

```python
class MODIPlusWeb(MODIPlus):
    def set_send_callback(self, callback): ...
    def on_message(self, data): ...
```

### PostMessageTask

Communication task for JavaScript postMessage integration.

```python
class PostMessageTask(ConnectionTask):
    def set_send_callback(self, callback): ...
    def on_message(self, data): ...
    def send(self, pkt): ...
    def recv(self): ...
```

## Requirements

- Python >= 3.8
- pymodi-plus (automatically installed)

## License

MIT License - see LICENSE file for details.

## Related Projects

- [pymodi-plus](https://github.com/LUXROBO/pymodi-plus) - Desktop version with USB/BLE support
- [modi_flutter](https://github.com/LUXROBO/modi_flutter) - Flutter app with WebUSB support
