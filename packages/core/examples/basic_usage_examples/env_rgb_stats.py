"""Example of using Env module RGB and color properties

This example demonstrates how to use the color sensor properties
of the Env module including:
- RGB (red, green, blue) values
- White and Black values
- Color class detection (red/green/blue/white/black/unknown)
- Brightness value

Note: These properties are only available in version 2.x and above.
This example tests ALL connected Env modules.
"""

import os
import sys

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import modi_plus
import time

# --- OS 구분 ---
IS_WINDOWS = (os.name == "nt")

if IS_WINDOWS:
    import msvcrt
else:
    import termios
    import tty
    import select


# ---------------------------------------------------------------------------
# Statistics helpers (refactored from globals -> class)
# ---------------------------------------------------------------------------

@dataclass
class RunningStat:
    """min/max/avg용 누적 통계"""
    min: Optional[int] = None
    max: Optional[int] = None
    sum: int = 0
    count: int = 0

    def update(self, value: int) -> None:
        if self.min is None or value < self.min:
            self.min = value
        if self.max is None or value > self.max:
            self.max = value
        self.sum += int(value)
        self.count += 1

    @property
    def avg(self) -> float:
        return (self.sum / self.count) if self.count else 0.0


class EnvStats:
    """Env RGB/조도 측정값 + color_name count 통계를 관리"""

    def __init__(self, metric_names=None) -> None:
        if metric_names is None:
            metric_names = ("raw_r", "raw_g", "raw_b", "raw_w", "r", "g", "b", "white", "black", "brightness")
        self._metric_names = tuple(metric_names)
        self.reset()

    def reset(self) -> None:
        # 숫자 통계
        self.metrics: Dict[str, RunningStat] = {n: RunningStat() for n in self._metric_names}
        # color_name 통계
        self.color_counts: Dict[str, int] = {}

    def update_metric(self, name: str, value: int) -> None:
        if name not in self.metrics:
            # 오타/새 항목이 들어와도 안전하게 처리
            self.metrics[name] = RunningStat()
        self.metrics[name].update(value)

    def update_color(self, color_name: Optional[str]) -> None:
        if not color_name:
            color_name = "None"
        self.color_counts[color_name] = self.color_counts.get(color_name, 0) + 1

    def top_color(self) -> Tuple[str, int]:
        if not self.color_counts:
            return ("N/A", 0)
        name, cnt = max(self.color_counts.items(), key=lambda x: x[1])
        return (name, cnt)

    def print_stats(self) -> None:
        """현재까지 누적된 통계 출력"""
        print("\n\n=== Measurement Statistics ===")
        for name in self._metric_names:
            s = self.metrics[name]
            if s.count == 0:
                print(f"{name:10s}: no data")
            else:
                print(f"{name:10s} min={s.min:4d}  max={s.max:4d}  avg={s.avg:8.2f}  (n={s.count})")

        # color_name 통계
        print("\n=== Color Name Counts ===")
        if not self.color_counts:
            print("no color data")
            return

        sorted_colors = sorted(self.color_counts.items(), key=lambda x: -x[1])
        max_count = sorted_colors[0][1] if sorted_colors else 0
        top_color = sorted_colors[0][0] if sorted_colors else "N/A"

        for cname, cnt in sorted_colors:
            line = f"{cname:10s}: {cnt:5d}"
            if cnt == max_count:
                line += "  <== The top-ranked color"
            print(line)

        # 요약 한줄
        raw_r = self.metrics["raw_r"].avg
        raw_g = self.metrics["raw_g"].avg
        raw_b = self.metrics["raw_b"].avg
        raw_w = self.metrics["raw_w"].avg

        r = self.metrics["r"].avg
        g = self.metrics["g"].avg
        b = self.metrics["b"].avg
        w = self.metrics["white"].avg
        k = self.metrics["black"].avg
        print("\n[Summary] RAW_R,RAW_G,RAW_B,RAW_W,R,G,B,W,K Avg,Top Color")
        print(f"{raw_r:.1f},{raw_g:.1f},{raw_b:.1f},{raw_w:.1f},", end="")
        print(f"{r:.1f},{g:.1f},{b:.1f},{w:.1f},{k:.1f},{top_color}")


# 통계 인스턴스 딕셔너리: module_idx -> EnvStats
# rgb_supported_modules 기준으로 동적 생성
stats_by_module: Dict[int, EnvStats] = {}


def get_stats(module_idx: int) -> EnvStats:
    """모듈 인덱스에 해당하는 EnvStats 반환 (없으면 생성)"""
    if module_idx not in stats_by_module:
        stats_by_module[module_idx] = EnvStats()
    return stats_by_module[module_idx]


def reset_all_stats() -> None:
    """모든 모듈의 통계 초기화"""
    for s in stats_by_module.values():
        s.reset()


def print_all_stats() -> None:
    """모든 모듈의 통계 출력"""
    for module_idx, s in sorted(stats_by_module.items()):
        print(f"\n{'#' * 60}")
        print(f"# Module #{module_idx + 1} Statistics")
        print(f"{'#' * 60}")
        s.print_stats()
def get_key_nonblocking():
    """
    - 키가 눌리면: 1글자(str) 반환
    - 아무 키도 없으면: None 반환
    """
    if IS_WINDOWS:
        # Windows: msvcrt 사용
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            try:
                return ch.decode(errors="ignore")
            except Exception:
                return None
        return None
    else:
        # macOS / Linux: select + cbreak 모드에서 stdin 읽기
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1)
        return None


# --- macOS / Linux에서는 터미널 모드 변경 필요(cbreak) ---
if not IS_WINDOWS:
    fd = sys.stdin.fileno()
    old_term_attr = termios.tcgetattr(fd)
    tty.setcbreak(fd)  # Enter 없이 한 글자씩 읽히도록

def test_env_module(env, index):
    """Test a single Env module for RGB support"""
    print(f"\n{'=' * 60}")
    print(f"Env Module #{index + 1} (ID: 0x{env.id:X})")
    print(f"{'=' * 60}")
    print(f"App Version: {env.app_version}")

    # Check if version supports RGB
    if hasattr(env, '_is_rgb_supported') and env._is_rgb_supported():
        print("✓ RGB properties are supported!")
        return True
    else:
        print("✗ RGB properties are NOT supported in this version")
        print("Please upgrade firmware to version 2.x or above")
        print("\nAvailable properties:")
        print(f"  - Temperature: {env.temperature}°C")
        print(f"  - Humidity: {env.humidity}%")
        print(f"  - Illuminance: {env.illuminance} lux")
        print(f"  - Volume: {env.volume} dB")
        return False


if __name__ == "__main__":
    bundle = modi_plus.MODIPlus()

    print("=" * 60)
    print("Env Module Color Sensor Example - Multi-Module Support")
    print("=" * 60)

    # Check how many Env modules are connected
    num_envs = len(bundle.envs)
    print(f"\nFound {num_envs} Env module(s)")

    if num_envs == 0:
        print("Error: No Env modules found!")
        bundle.close()
        exit(1)

    # Test each Env module
    rgb_supported_modules = []
    for i, env in enumerate(bundle.envs):
        if test_env_module(env, i):
            rgb_supported_modules.append((i, env))

    stop_flag = False

    # If any module supports RGB, start continuous reading
    if rgb_supported_modules:
        print(f"\n{'=' * 60}")
        print(f"Reading color sensor values from {len(rgb_supported_modules)} module(s)")
        print("Press Ctrl+C to stop")
        print(f"{'=' * 60}\n")

        # Color class 이름 매핑
        color_names = {
            0: "unknown",
            1: "red",
            2: "green",
            3: "blue",
            4: "white",
            5: "black"
        }

        # 각 모듈별 통계 초기화
        for idx, env in rgb_supported_modules:
            get_stats(idx).reset()
        stats_count = 0
        try:
            while True:
                ch = get_key_nonblocking()
                if ch is not None:
                    ch = ch.lower()
                    if ch == 'q':
                        print("\n\nStop command received. Exiting...")
                        break
                    elif ch == 's':
                        stop_flag = not stop_flag
                        if stop_flag:
                            print("\nReading paused. Press 's' to resume.")
                            print_all_stats()
                            reset_all_stats()
                            stats_count = 0
                        else:
                            reset_all_stats()
                            stats_count = 0
                            print("\nReading resumed.")
                elif stats_count >= 100:
                    stop_flag = True
                    print_all_stats()
                    reset_all_stats()
                    stats_count = 0

                if stop_flag:
                    time.sleep(0.1)
                    continue

                # Read and display all color properties from all supported modules
                for idx, env in rgb_supported_modules:
                    # env.set_rgb_mode(env.RGB_MODE_DUALSHOT)
                    env.set_rgb_mode(env.RGB_MODE_ON, 300)
                    try:
                        r, g, b = env.rgb
                        raw_r, raw_g, raw_b, raw_w = env.raw_rgb
                        white = env.white
                        black = env.black
                        color_class = env.color_class
                        brightness = env.brightness
                        color_name = color_names.get(color_class, "unknown")

                        # --- 모듈별 통계 갱신 ---
                        module_stats = get_stats(idx)
                        module_stats.update_metric("raw_r", raw_r)
                        module_stats.update_metric("raw_g", raw_g)
                        module_stats.update_metric("raw_b", raw_b)
                        module_stats.update_metric("raw_w", raw_w)

                        module_stats.update_metric("r", r)
                        module_stats.update_metric("g", g)
                        module_stats.update_metric("b", b)
                        module_stats.update_metric("white", white)
                        module_stats.update_metric("black", black)
                        module_stats.update_metric("brightness", brightness)
                        module_stats.update_color(color_name)

                        print(f"Module #{idx + 1}: ", end="")
                        print(f"RAW_RGB=({raw_r:5d},{raw_g:5d},{raw_b:5d},{raw_w:5d}) ", end="")
                        print(f"RGB=({r:3d},{g:3d},{b:3d}) ", end="")
                        print(f"W={white:3d} B={black:3d} ", end="")
                        print(f"Bright={brightness:3d} ", end="")
                        print(f"Color={color_name:7s}", end="  ")
                        stats_count += 1
                    except Exception as e:
                        print(f"Module #{idx + 1}: Error - {e}", end="  ")

                print("\r", end="", flush=True)
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n\nStopped by user")

    else:
        print(f"\n{'=' * 60}")
        print("No modules with RGB support found.")
        print("All connected modules are version 1.x")
        print(f"{'=' * 60}")

    bundle.close()