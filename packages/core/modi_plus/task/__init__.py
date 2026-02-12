"""MODI+ Task module - 통신 레이어

조건부 import를 통해 pyserial/bleak 없이도 패키지 import 가능
"""

# 플래그 초기화
HAS_SERIAL = False
HAS_BLE = False

# Serial Task (pyserial 필요)
try:
    from modi_plus.task.serialport_task import SerialportTask
    HAS_SERIAL = True
except ImportError:
    SerialportTask = None

# BLE Task (bleak 필요)
try:
    from modi_plus.util.connection_util import get_ble_task_path
    from importlib import import_module
    # BLE task는 플랫폼별로 다르므로 여기서 직접 import하지 않음
    HAS_BLE = True
except ImportError:
    HAS_BLE = False

# Connection Task (항상 사용 가능)
from modi_plus.task.connection_task import ConnectionTask

__all__ = [
    'ConnectionTask',
    'HAS_SERIAL',
    'HAS_BLE',
    'SerialportTask',
]
