"""MODIPlusWeb 단위 테스트"""

import unittest
from unittest.mock import MagicMock, patch
import json

from modi_plus_web.task.postmessage_task import PostMessageTask
from modi_plus_web.modi_plus_web import MODIPlusWeb


class TestMODIPlusWeb(unittest.TestCase):
    """MODIPlusWeb 클래스 테스트"""

    def setUp(self):
        """각 테스트 전 실행 - MODIPlus import 모킹"""
        # MODIPlus가 하드웨어 연결을 시도하지 않도록 모킹
        self.mock_modi_plus_patcher = patch('modi_plus_web.modi_plus_web.MODIPlus.__init__')
        self.mock_modi_plus = self.mock_modi_plus_patcher.start()
        self.mock_modi_plus.return_value = None

    def tearDown(self):
        """각 테스트 후 실행"""
        self.mock_modi_plus_patcher.stop()

    def test_initialization(self):
        """초기화 테스트"""
        modi = MODIPlusWeb()

        self.assertIsNotNone(modi._postmessage_task)
        self.assertIsInstance(modi._postmessage_task, PostMessageTask)

    def test_task_property(self):
        """task 프로퍼티 테스트"""
        modi = MODIPlusWeb()

        self.assertIsInstance(modi.task, PostMessageTask)
        self.assertEqual(modi.task, modi._postmessage_task)

    def test_set_send_callback(self):
        """set_send_callback 메서드 테스트"""
        modi = MODIPlusWeb()

        callback = MagicMock()
        modi.set_send_callback(callback)

        self.assertEqual(modi._postmessage_task._send_callback, callback)

    def test_on_message(self):
        """on_message 메서드 테스트"""
        modi = MODIPlusWeb()

        test_data = '{"c":0,"s":1,"d":2}'
        modi.on_message(test_data)

        received = modi._postmessage_task.recv()
        self.assertEqual(received, test_data)

    def test_verbose_mode(self):
        """verbose 모드 전달 테스트"""
        modi = MODIPlusWeb(verbose=True)

        self.assertTrue(modi._postmessage_task.verbose)


class TestMODIPlusWebIntegration(unittest.TestCase):
    """MODIPlusWeb 통합 테스트 (모킹 없이)"""

    @patch('modi_plus_web.modi_plus_web.MODIPlus.__init__')
    def test_full_workflow(self, mock_init):
        """전체 워크플로우 테스트"""
        mock_init.return_value = None

        modi = MODIPlusWeb()

        # 콜백 설정
        sent_packets = []
        modi.set_send_callback(lambda pkt: sent_packets.append(pkt))

        # 외부 메시지 수신
        modi.on_message('{"c":0,"s":100,"d":0}')

        # 내부에서 처리
        received = modi.task.recv()
        self.assertIsNotNone(received)

        # 응답 전송
        modi.task.send('{"c":4,"s":0,"d":100}')

        self.assertEqual(len(sent_packets), 1)


if __name__ == '__main__':
    unittest.main()
