"""PostMessageTask 단위 테스트"""

import unittest
import json
from modi_plus_web.task.postmessage_task import PostMessageTask


class TestPostMessageTask(unittest.TestCase):
    """PostMessageTask 클래스 테스트"""

    def setUp(self):
        """각 테스트 전 실행"""
        self.task = PostMessageTask()

    def tearDown(self):
        """각 테스트 후 실행"""
        self.task.close_connection()

    # ===================
    # 연결 테스트
    # ===================
    def test_initial_state(self):
        """초기 상태 테스트"""
        self.assertFalse(self.task.is_connected)
        self.assertIsNone(self.task._send_callback)
        self.assertTrue(self.task._recv_queue.empty())

    def test_open_connection(self):
        """연결 열기 테스트"""
        self.task.open_connection()
        self.assertTrue(self.task.is_connected)

    def test_close_connection(self):
        """연결 닫기 테스트"""
        self.task.open_connection()
        self.task.close_connection()
        self.assertFalse(self.task.is_connected)
        self.assertIsNone(self.task._send_callback)

    # ===================
    # 메시지 수신 테스트
    # ===================
    def test_on_message_with_string(self):
        """JSON 문자열 수신 테스트"""
        self.task.open_connection()
        test_msg = '{"c":0,"s":1,"d":2,"b":"AA==","l":1}'

        self.task.on_message(test_msg)

        self.assertFalse(self.task._recv_queue.empty())
        received = self.task.recv()
        self.assertEqual(received, test_msg)

    def test_on_message_with_dict(self):
        """딕셔너리 수신 테스트"""
        self.task.open_connection()
        test_data = {"c": 0, "s": 1, "d": 2, "b": "AA==", "l": 1}

        self.task.on_message(test_data)

        received = self.task.recv()
        self.assertEqual(json.loads(received), test_data)

    def test_on_message_invalid_json(self):
        """유효하지 않은 JSON 테스트"""
        self.task.open_connection()
        self.task.verbose = True  # 디버그 모드

        self.task.on_message("invalid json {{{")

        # 유효하지 않은 JSON은 무시됨
        self.assertTrue(self.task._recv_queue.empty())

    def test_recv_empty_queue(self):
        """빈 큐에서 수신 테스트"""
        self.task.open_connection()
        received = self.task.recv()
        self.assertIsNone(received)

    def test_recv_multiple_messages(self):
        """다중 메시지 수신 테스트"""
        self.task.open_connection()
        messages = [
            '{"c":0,"s":1}',
            '{"c":1,"s":2}',
            '{"c":2,"s":3}',
        ]

        for msg in messages:
            self.task.on_message(msg)

        for expected in messages:
            received = self.task.recv()
            self.assertEqual(received, expected)

        # 큐가 비어있어야 함
        self.assertIsNone(self.task.recv())

    # ===================
    # 메시지 전송 테스트
    # ===================
    def test_send_without_callback(self):
        """콜백 없이 전송 테스트"""
        self.task.open_connection()
        # 콜백 없이 send해도 에러 없어야 함
        self.task.send('{"test": 1}')

    def test_send_with_callback(self):
        """콜백 있을 때 전송 테스트"""
        self.task.open_connection()
        sent_messages = []

        def mock_callback(pkt):
            sent_messages.append(pkt)

        self.task.set_send_callback(mock_callback)

        test_pkt = '{"c":4,"s":0,"d":1234}'
        self.task.send(test_pkt)

        self.assertEqual(len(sent_messages), 1)
        self.assertEqual(sent_messages[0], test_pkt)

    def test_send_nowait(self):
        """send_nowait 테스트 (send와 동일 동작)"""
        self.task.open_connection()
        sent_messages = []

        self.task.set_send_callback(lambda pkt: sent_messages.append(pkt))
        self.task.send_nowait('{"test": 1}')

        self.assertEqual(len(sent_messages), 1)

    # ===================
    # 콜백 테스트
    # ===================
    def test_set_send_callback(self):
        """콜백 설정 테스트"""
        callback = lambda x: x
        self.task.set_send_callback(callback)
        self.assertEqual(self.task._send_callback, callback)

    def test_callback_cleared_on_close(self):
        """연결 종료 시 콜백 초기화 테스트"""
        self.task.set_send_callback(lambda x: x)
        self.task.open_connection()
        self.task.close_connection()
        self.assertIsNone(self.task._send_callback)

    # ===================
    # verbose 모드 테스트
    # ===================
    def test_verbose_mode(self):
        """verbose 모드 테스트"""
        task = PostMessageTask(verbose=True)
        self.assertTrue(task.verbose)

        task2 = PostMessageTask(verbose=False)
        self.assertFalse(task2.verbose)


class TestPostMessageTaskIntegration(unittest.TestCase):
    """PostMessageTask 통합 테스트"""

    def test_full_communication_cycle(self):
        """전체 통신 사이클 테스트"""
        task = PostMessageTask()
        task.open_connection()

        # 콜백 설정
        responses = []
        task.set_send_callback(lambda pkt: responses.append(pkt))

        # 메시지 수신 (외부에서 온 것 시뮬레이션)
        incoming = {"c": 0, "s": 100, "d": 0, "b": "VEVTVA==", "l": 4}
        task.on_message(incoming)

        # 메시지 처리
        received = task.recv()
        data = json.loads(received)

        # 응답 전송
        response = {"c": 4, "s": 0, "d": data["s"], "b": "T0s=", "l": 2}
        task.send(json.dumps(response))

        # 검증
        self.assertEqual(len(responses), 1)
        sent_data = json.loads(responses[0])
        self.assertEqual(sent_data["d"], 100)  # 원래 소스로 응답

        task.close_connection()


if __name__ == '__main__':
    unittest.main()
