"""MODIPlusWeb - 웹 환경용 MODI+ 클래스

pymodi-plus의 MODIPlus를 상속하여 PostMessageTask를 기본 통신 레이어로 사용합니다.
Pyodide 환경에서 JavaScript와 postMessage를 통해 MODI+ 모듈과 통신할 수 있습니다.
"""

from typing import Callable, Optional

from modi_plus import MODIPlus
from modi_plus_web.task.postmessage_task import PostMessageTask


class MODIPlusWeb(MODIPlus):
    """웹 환경용 MODI+ 클래스

    PostMessageTask를 사용하여 JavaScript와 postMessage로 통신합니다.
    modi_flutter의 WebUSB와 연동하여 MODI+ 모듈을 제어할 수 있습니다.

    Usage:
        from modi_plus_web import MODIPlusWeb

        modi = MODIPlusWeb()

        # JavaScript 콜백 설정
        import js
        modi.set_send_callback(lambda pkt: js.postMessage({'type': 'modi', 'data': pkt}))

        # 표준 MODI+ API 사용
        led = modi.led(0x1234)
        led.rgb = (255, 0, 0)
    """

    def __init__(self, verbose: bool = False):
        """MODIPlusWeb 초기화

        Args:
            verbose: 디버그 메시지 출력 여부
        """
        # PostMessageTask를 주입하여 부모 클래스 초기화
        self._postmessage_task = PostMessageTask(verbose=verbose)
        super().__init__(task=self._postmessage_task, verbose=verbose)

    @property
    def task(self) -> PostMessageTask:
        """PostMessageTask 인스턴스 접근"""
        return self._postmessage_task

    def set_send_callback(self, callback: Callable[[str], None]) -> None:
        """JavaScript로 메시지를 전송할 콜백 함수 설정

        Args:
            callback: 메시지를 받아 JavaScript로 전송하는 함수

        Example:
            import js
            modi.set_send_callback(lambda pkt: js.postMessage({'type': 'modi', 'data': pkt}))
        """
        self._postmessage_task.set_send_callback(callback)

    def on_message(self, data) -> None:
        """JavaScript에서 메시지 수신 시 호출

        Args:
            data: 수신된 데이터 (JSON 문자열 또는 dict)

        Example:
            # JavaScript에서
            pyodide.runPython(`modi.on_message('${jsonData}')`)
        """
        self._postmessage_task.on_message(data)
