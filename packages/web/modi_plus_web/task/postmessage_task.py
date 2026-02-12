"""PostMessageTask - JavaScript postMessage 통신용 Task

Pyodide 환경에서 JavaScript와 postMessage를 통해 통신하는 Task 클래스입니다.
modi_flutter의 WebUSB와 연동하여 MODI+ 모듈과 통신할 수 있습니다.
"""

from queue import Queue
from typing import Optional, Callable
import json

from modi_plus.task.connection_task import ConnectionTask


class PostMessageTask(ConnectionTask):
    """JavaScript postMessage 통신용 Task

    Pyodide 환경에서 JavaScript와 postMessage를 통해 통신합니다.

    Usage:
        task = PostMessageTask()

        # JavaScript에서 Python으로 메시지 전달
        task.on_message('{"c":0,"s":1,"d":2,"b":"AA==","l":1}')

        # Python에서 JavaScript로 메시지 전달
        task.set_send_callback(lambda pkt: js.postMessage(pkt))
        task.send('{"c":0,"s":1,"d":2,"b":"AA==","l":1}')
    """

    def __init__(self, verbose: bool = False):
        """PostMessageTask 초기화

        Args:
            verbose: 디버그 메시지 출력 여부
        """
        super().__init__(verbose)
        self._recv_queue: Queue = Queue()
        self._send_callback: Optional[Callable[[str], None]] = None
        self._connected: bool = False

    def set_send_callback(self, callback: Callable[[str], None]) -> None:
        """JavaScript로 메시지를 전송할 콜백 함수 설정

        Args:
            callback: 메시지를 받아 JavaScript로 전송하는 함수

        Example:
            # Pyodide에서
            import js
            task.set_send_callback(lambda pkt: js.postMessage({'type': 'modi', 'data': pkt}))
        """
        self._send_callback = callback

    def on_message(self, data) -> None:
        """JavaScript에서 메시지 수신 시 호출

        Args:
            data: 수신된 데이터 (JSON 문자열 또는 dict)

        Example:
            # JavaScript에서
            pyodide.runPython(`task.on_message('${jsonData}')`)
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        elif isinstance(data, str):
            # 이미 JSON 문자열인 경우 그대로 사용
            try:
                # 유효한 JSON인지 확인
                json.loads(data)
            except json.JSONDecodeError:
                if self.verbose:
                    print(f"Invalid JSON received: {data}")
                return
        else:
            if self.verbose:
                print(f"Unsupported data type: {type(data)}")
            return

        self._recv_queue.put(data)

        if self.verbose:
            print(f"on_message: {data}")

    def open_connection(self) -> None:
        """연결 시작 (JavaScript 측에서 WebUSB 연결 처리)"""
        self._connected = True
        self._recv_queue = Queue()
        if self.verbose:
            print("PostMessageTask connection opened")

    def close_connection(self) -> None:
        """연결 종료"""
        self._connected = False
        self._send_callback = None
        if self.verbose:
            print("PostMessageTask connection closed")

    def recv(self) -> Optional[str]:
        """수신 큐에서 메시지 가져오기

        Returns:
            JSON 문자열 또는 None (큐가 비어있는 경우)
        """
        if self._recv_queue.empty():
            return None

        json_pkt = self._recv_queue.get()

        if self.verbose:
            print(f"recv: {json_pkt}")

        return json_pkt

    def send(self, pkt: str, verbose: bool = False) -> None:
        """JavaScript로 메시지 전송

        Args:
            pkt: 전송할 JSON 패킷
            verbose: 디버그 메시지 출력 여부
        """
        if self._send_callback:
            self._send_callback(pkt)

            if self.verbose or verbose:
                print(f"send: {pkt}")
        else:
            if self.verbose or verbose:
                print(f"send (no callback): {pkt}")

    def send_nowait(self, pkt: str, verbose: bool = False) -> None:
        """JavaScript로 메시지 전송 (send와 동일)

        Args:
            pkt: 전송할 JSON 패킷
            verbose: 디버그 메시지 출력 여부
        """
        self.send(pkt, verbose)

    @property
    def is_connected(self) -> bool:
        """연결 상태 확인"""
        return self._connected
