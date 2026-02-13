"""pymodi-plus-web - MODI+ Python Library for Web/Pyodide

This package provides web-compatible communication layer for pymodi-plus,
enabling MODI+ hardware control through JavaScript postMessage in Pyodide environments.
"""

from modi_plus_web.modi_plus_web import MODIPlusWeb
from modi_plus_web.task.postmessage_task import PostMessageTask

__version__ = "0.1.0"
__all__ = ["MODIPlusWeb", "PostMessageTask"]

print(f"Running PyMODI+ Web (v{__version__})")
