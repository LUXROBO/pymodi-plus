# PyMODI+ Web 배포 및 사용 가이드

## 목차
1. [개요](#개요)
2. [내부 테스트 배포](#내부-테스트-배포)
3. [설치 방법](#설치-방법)
4. [사용 방법](#사용-방법)
5. [Pyodide 통합](#pyodide-통합)
6. [Flutter 연동](#flutter-연동)
7. [트러블슈팅](#트러블슈팅)

---

## 개요

`pymodi-plus-web`은 웹 브라우저 환경(Pyodide)에서 MODI+ 모듈을 제어하기 위한 패키지입니다.

### 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                      Web Browser                             │
│  ┌─────────────┐    postMessage    ┌─────────────────────┐  │
│  │   Pyodide   │ ◄───────────────► │  JavaScript/Flutter │  │
│  │  (Python)   │                   │     (WebUSB)        │  │
│  └─────────────┘                   └─────────────────────┘  │
│        │                                     │               │
│        ▼                                     ▼               │
│  ┌─────────────┐                   ┌─────────────────────┐  │
│  │ pymodi-plus │                   │    MODI+ Hardware   │  │
│  │    -web     │                   │    (via WebUSB)     │  │
│  └─────────────┘                   └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 패키지 구조

```
pymodi-plus-web/
├── modi_plus_web/
│   ├── __init__.py
│   ├── modi_plus_web.py      # MODIPlusWeb 클래스
│   └── task/
│       ├── __init__.py
│       └── postmessage_task.py  # PostMessageTask 통신 레이어
└── tests/
```

---

## 내부 테스트 배포

### 방법 1: TestPyPI (권장)

TestPyPI는 PyPI의 테스트 서버로, 실제 배포 전 테스트용으로 사용합니다.

#### 1단계: TestPyPI 계정 설정

```bash
# ~/.pypirc 파일 생성
cat > ~/.pypirc << 'EOF'
[testpypi]
username = __token__
password = pypi-YOUR_TEST_PYPI_TOKEN
EOF
```

#### 2단계: 패키지 빌드

```bash
cd packages/web
rm -rf dist build *.egg-info
python -m build
```

#### 3단계: TestPyPI에 업로드

```bash
python -m twine upload --repository testpypi dist/*
```

#### 4단계: TestPyPI에서 설치 테스트

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pymodi-plus-web
```

### 방법 2: Git에서 직접 설치

브랜치에서 직접 설치하는 방법입니다.

```bash
# pymodi-plus (core) 설치 - 변경된 버전
pip install git+https://github.com/LUXROBO/pymodi-plus.git@feature/web-support

# pymodi-plus-web 설치
pip install git+https://github.com/LUXROBO/pymodi-plus.git@feature/web-support#subdirectory=packages/web
```

### 방법 3: 로컬 wheel 파일

빌드된 wheel 파일을 직접 공유하는 방법입니다.

```bash
# 빌드
cd packages/web
python -m build

# 설치 (wheel 파일 경로)
pip install dist/pymodi_plus_web-0.1.0-py3-none-any.whl
```

---

## 설치 방법

### 데스크톱 환경

```bash
# pymodi-plus-web 설치 (pymodi-plus 자동 설치됨)
pip install pymodi-plus-web
```

### Pyodide 환경 (웹 브라우저)

```python
import micropip

# pymodi-plus 설치 (최소 의존성)
await micropip.install('pymodi-plus')

# pymodi-plus-web 설치
await micropip.install('pymodi-plus-web')
```

---

## 사용 방법

### 기본 사용법

```python
from modi_plus_web import MODIPlusWeb

# 인스턴스 생성
modi = MODIPlusWeb(verbose=True)

# JavaScript로 메시지 전송할 콜백 설정
def send_to_js(packet):
    # JavaScript postMessage로 전송
    js.window.modiSend(packet)

modi.set_send_callback(send_to_js)

# JavaScript에서 메시지 수신 시 호출
def on_js_message(data):
    modi.on_message(data)

# 모듈 사용 (기존 pymodi-plus와 동일)
led = modi.leds[0]
led.turn_on()
led.set_rgb(255, 0, 0)
```

### PostMessageTask 직접 사용

```python
from modi_plus_web.task import PostMessageTask

# Task 직접 생성
task = PostMessageTask(verbose=True)
task.open_connection()

# 콜백 설정
task.set_send_callback(lambda pkt: print(f"Send: {pkt}"))

# 메시지 수신
task.on_message('{"c":0,"s":100,"d":0}')

# 메시지 처리
received = task.recv()
print(f"Received: {received}")

# 메시지 전송
task.send('{"c":4,"s":0,"d":100}')
```

---

## Pyodide 통합

### HTML 템플릿

```html
<!DOCTYPE html>
<html>
<head>
    <title>PyMODI+ Web</title>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
</head>
<body>
    <div id="output"></div>

    <script>
    // 전역 변수
    let pyodide = null;
    let modi = null;

    // Python으로 메시지 전송 (하드웨어 → Python)
    function sendToPython(data) {
        if (pyodide && modi) {
            pyodide.runPython(`modi.on_message('${JSON.stringify(data)}')`);
        }
    }

    // JavaScript에서 하드웨어로 전송 (Python → 하드웨어)
    window.modiSend = function(packet) {
        console.log('To hardware:', packet);
        // WebUSB 또는 Flutter로 전송
        // flutterChannel.postMessage(packet);
    };

    async function main() {
        // Pyodide 로드
        pyodide = await loadPyodide();

        // 패키지 설치
        await pyodide.loadPackage('micropip');
        await pyodide.runPythonAsync(`
            import micropip
            await micropip.install('pymodi-plus')
            await micropip.install('pymodi-plus-web')
        `);

        // MODI+ 초기화
        await pyodide.runPythonAsync(`
            from modi_plus_web import MODIPlusWeb
            import js

            modi = MODIPlusWeb(verbose=True)
            modi.set_send_callback(lambda pkt: js.window.modiSend(pkt))
        `);

        // 전역 참조 저장
        modi = pyodide.globals.get('modi');

        console.log('PyMODI+ Web initialized!');
    }

    main();
    </script>
</body>
</html>
```

### Python 코드 실행

```javascript
// JavaScript에서 Python 코드 실행
async function runPythonCode(code) {
    try {
        const result = await pyodide.runPythonAsync(code);
        return result;
    } catch (error) {
        console.error('Python error:', error);
        throw error;
    }
}

// 예시: LED 제어
await runPythonCode(`
led = modi.leds[0]
led.turn_on()
led.set_rgb(255, 0, 0)
`);
```

---

## Flutter 연동

### Flutter → Pyodide 통신

```dart
// Flutter (Dart)
import 'package:webview_flutter/webview_flutter.dart';

class ModiWebView extends StatefulWidget {
  @override
  _ModiWebViewState createState() => _ModiWebViewState();
}

class _ModiWebViewState extends State<ModiWebView> {
  late WebViewController controller;

  @override
  void initState() {
    super.initState();
    controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..addJavaScriptChannel(
        'ModiChannel',
        onMessageReceived: (message) {
          // Python에서 온 메시지 → 하드웨어로 전송
          _sendToHardware(message.message);
        },
      )
      ..loadFlutterAsset('assets/pyodide.html');
  }

  // 하드웨어에서 온 메시지 → Python으로 전송
  void sendToPython(String data) {
    controller.runJavaScript('sendToPython($data)');
  }

  void _sendToHardware(String packet) {
    // WebUSB 또는 시리얼 통신으로 전송
  }
}
```

### JavaScript Bridge 설정

```javascript
// pyodide.html 내 JavaScript
window.modiSend = function(packet) {
    // Flutter로 전송
    if (window.ModiChannel) {
        ModiChannel.postMessage(packet);
    }
};
```

---

## 트러블슈팅

### 1. micropip 설치 오류

**증상:**
```
ValueError: Can't find a pure Python 3 wheel for 'pymodi-plus'
```

**해결:**
pymodi-plus가 pure Python wheel로 빌드되어야 합니다. TestPyPI나 PyPI에서 올바른 버전을 확인하세요.

### 2. JavaScript 콜백 오류

**증상:**
```
AttributeError: 'JsProxy' object has no attribute 'js_send'
```

**해결:**
`js.window.modiSend` 형식으로 전역 함수를 호출하세요:
```python
modi.set_send_callback(lambda pkt: js.window.modiSend(pkt))
```

### 3. 모듈을 찾을 수 없음

**증상:**
```
IndexError: list index out of range (modi.leds[0])
```

**해결:**
모듈 검색이 완료될 때까지 대기하거나, 하드웨어 연결 상태를 확인하세요:
```python
import time
time.sleep(2)  # 모듈 검색 대기
print(modi.modules)  # 연결된 모듈 확인
```

### 4. 메시지 형식 오류

**증상:**
```
json.JSONDecodeError: Expecting property name
```

**해결:**
JSON 형식이 올바른지 확인하세요:
```python
# 올바른 형식
modi.on_message('{"c":0,"s":100,"d":0}')

# 잘못된 형식
modi.on_message("{c:0,s:100,d:0}")  # 따옴표 누락
```

---

## 버전 호환성

| pymodi-plus | pymodi-plus-web | Python | Pyodide |
|-------------|-----------------|--------|---------|
| >= 0.5.0    | 0.1.0           | >= 3.8 | >= 0.24 |

---

## 참고 자료

- [PyMODI+ GitHub](https://github.com/LUXROBO/pymodi-plus)
- [Pyodide 공식 문서](https://pyodide.org/)
- [WebUSB API](https://developer.mozilla.org/en-US/docs/Web/API/WebUSB_API)
