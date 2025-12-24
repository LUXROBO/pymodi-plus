"""
Real-time RGB Model Testing Script

This script tests the trained RGB calibration model with live sensor data.
It reads raw sensor values, applies the trained model, and compares the 
predicted RGB values with the actual sensor RGB values.
"""

import os
import sys
import pickle
import time
import argparse
from typing import Dict, Optional

# Add parent directory to path to import modi_plus
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import modi_plus
import numpy as np

# --- OS 구분 ---
IS_WINDOWS = (os.name == "nt")

if IS_WINDOWS:
    import msvcrt
else:
    import termios
    import tty
    import select


class RGBConverter:
    """RGB color space conversion and Black/White calculation utilities"""
    
    @staticmethod
    def rgb_255_to_100(r, g, b):
        """Convert RGB from 0-255 scale to 0-100 scale"""
        r_100 = int(round(r * 100 / 255))
        g_100 = int(round(g * 100 / 255))
        b_100 = int(round(b * 100 / 255))
        return r_100, g_100, b_100
    
    @staticmethod
    def calculate_black_white_method1(r, g, b):
        """
        Method 1: Color Theory Based
        White = minimum of all channels (common brightness)
        Black = darkness level (inverse of max brightness)
        """
        white = min(r, g, b)
        black = 255 - max(r, g, b)
        return int(white), int(black)
    
    @staticmethod
    def classify_color(r, g, b, white, black, threshold=50):
        """
        Classify color into basic RGB categories
        
        Args:
            r, g, b: RGB values (0-255)
            white: White component from Color Theory
            black: Black component from Color Theory
            threshold: Minimum difference to consider a color dominant
            
        Returns:
            Color name: Red, Green, Blue, White, Black, or Unknown
        """
        max_rgb = max(r, g, b)
        min_rgb = min(r, g, b)
        
        # Very dark -> Black
        if max_rgb < 40:
            return "Black"
        
        # Very bright and low saturation -> White
        if min_rgb > 180 and (max_rgb - min_rgb) < 50:
            return "White"
        
        # Check if signal is too weak or unclear
        if max_rgb < 60:
            return "Unknown"
        
        # Find the dominant color
        if r > g and r > b:
            # Red is dominant
            if r > (g + threshold) and r > (b + threshold):
                return "Red"
            else:
                return "Unknown"  # Not clearly red
        elif g > r and g > b:
            # Green is dominant
            if g > (r + threshold) and g > (b + threshold):
                return "Green"
            else:
                return "Unknown"  # Not clearly green
        elif b > r and b > g:
            # Blue is dominant
            if b > (r + threshold) and b > (g + threshold):
                return "Blue"
            else:
                return "Unknown"  # Not clearly blue
        else:
            # No clear dominant color
            return "Unknown"
    
    @staticmethod
    def calculate_black_white_method2(r, g, b):
        """
        Method 2: Brightness Based
        Brightness = average of RGB
        White = brightness
        Black = inverse of brightness
        """
        brightness = (r + g + b) / 3
        white = int(brightness)
        black = int(255 - brightness)
        return white, black
    
    @staticmethod
    def calculate_black_white_method3(r, g, b):
        """
        Method 3: HSV Value Based
        V (Value) = max(R, G, B)
        White = V
        Black = inverse of V
        """
        v = max(r, g, b)
        white = int(v)
        black = int(255 - v)
        return white, black
    
    @staticmethod
    def calculate_black_white_method4(r, g, b, raw_w):
        """
        Method 4: RAW_W sensor value based
        White = scaled RAW_W value
        Black = calculated from RGB brightness
        
        Assumes RAW_W range is approximately 0-5000
        """
        # Scale RAW_W to 0-255 range (assuming max ~5000)
        white = int(min(255, raw_w * 255 / 5000))
        
        # Black based on darkness (inverse of brightness)
        brightness = (r + g + b) / 3
        black = int(255 - brightness)
        
        return white, black
    
    @staticmethod
    def calculate_all_methods(r, g, b, raw_w):
        """Calculate Black/White using all methods for comparison"""
        methods = {
            'Method1_ColorTheory': RGBConverter.calculate_black_white_method1(r, g, b),
            'Method2_Brightness': RGBConverter.calculate_black_white_method2(r, g, b),
            'Method3_HSV': RGBConverter.calculate_black_white_method3(r, g, b),
            'Method4_RawW': RGBConverter.calculate_black_white_method4(r, g, b, raw_w),
        }
        return methods


class RGBModelPredictor:
    """Wrapper class for RGB prediction models"""
    
    def __init__(self, model_path, is_enhanced=False):
        """Load trained models from pickle file"""
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
        
        self.is_enhanced = is_enhanced
        
        if is_enhanced:
            # Enhanced model format
            self.models = data['models']
            self.feature_names = data['feature_names']
            self.sensor_specs = data['sensor_specs']
            self.feature_options = data['feature_options']
            print(f"✓ Enhanced models loaded from: {model_path}")
            print(f"  Features: {len(self.feature_names)}")
            print(f"  Lux normalization: {self.feature_options['lux_normalization']}")
            print(f"  White ratio: {self.feature_options['white_ratio']}")
            print(f"  Cross-channel: {self.feature_options['cross_channel']}")
        else:
            # Basic model format
            self.models = data
            print(f"✓ Basic models loaded from: {model_path}")
        
        self.model_r = self.models['r']
        self.model_g = self.models['g']
        self.model_b = self.models['b']
    
    def _engineer_features(self, raw_r, raw_g, raw_b, raw_w):
        """Engineer features for enhanced model"""
        features = []
        
        # Original raw values
        features.extend([raw_r, raw_g, raw_b, raw_w])
        
        if self.feature_options['lux_normalization']:
            # Lux calculation
            lux = raw_w * self.sensor_specs['sensitivity']
            features.append(lux)
            
            # Normalized by lux
            features.append(raw_r / (lux + 1))
            features.append(raw_g / (lux + 1))
            features.append(raw_b / (lux + 1))
        
        if self.feature_options['white_ratio']:
            # White channel ratios
            raw_w_safe = max(raw_w, 1)
            features.append(raw_r / raw_w_safe)
            features.append(raw_g / raw_w_safe)
            features.append(raw_b / raw_w_safe)
        
        if self.feature_options['cross_channel']:
            # Cross-channel features
            total = raw_r + raw_g + raw_b + 1e-6
            features.append(raw_r / total)  # DOM_R
            features.append(raw_g / total)  # DOM_G
            features.append(raw_b / total)  # DOM_B
            features.append(raw_r / (raw_g + 1))  # RG_RATIO
            features.append(raw_g / (raw_b + 1))  # GB_RATIO
            features.append(raw_r / (raw_b + 1))  # RB_RATIO
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, raw_r, raw_g, raw_b, raw_w):
        """
        Predict RGB values from raw sensor readings
        
        Args:
            raw_r, raw_g, raw_b, raw_w: Raw sensor values
            
        Returns:
            Tuple of (predicted_r, predicted_g, predicted_b)
        """
        if self.is_enhanced:
            # Use engineered features
            X = self._engineer_features(raw_r, raw_g, raw_b, raw_w)
        else:
            # Use raw features only
            X = [[raw_r, raw_g, raw_b, raw_w]]
        
        # Predict each channel
        pred_r = self.model_r.predict(X)[0]
        pred_g = self.model_g.predict(X)[0]
        pred_b = self.model_b.predict(X)[0]
        
        # Clip to valid range [0, 255]
        pred_r = max(0, min(255, pred_r))
        pred_g = max(0, min(255, pred_g))
        pred_b = max(0, min(255, pred_b))
        
        return int(pred_r), int(pred_g), int(pred_b)
    
    def get_coefficients(self):
        """Get model coefficients for debugging"""
        return {
            'r': {'weights': self.model_r.coef_, 'bias': self.model_r.intercept_},
            'g': {'weights': self.model_g.coef_, 'bias': self.model_g.intercept_},
            'b': {'weights': self.model_b.coef_, 'bias': self.model_b.intercept_}
        }


class PerformanceTracker:
    """Track prediction errors and statistics"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.errors_r = []
        self.errors_g = []
        self.errors_b = []
        self.count = 0
    
    def update(self, actual_r, actual_g, actual_b, pred_r, pred_g, pred_b):
        """Update with new prediction"""
        self.errors_r.append(abs(actual_r - pred_r))
        self.errors_g.append(abs(actual_g - pred_g))
        self.errors_b.append(abs(actual_b - pred_b))
        self.count += 1
    
    def get_stats(self):
        """Get current statistics"""
        if self.count == 0:
            return None
        
        import numpy as np
        return {
            'count': self.count,
            'mae_r': np.mean(self.errors_r),
            'mae_g': np.mean(self.errors_g),
            'mae_b': np.mean(self.errors_b),
            'max_error_r': np.max(self.errors_r),
            'max_error_g': np.max(self.errors_g),
            'max_error_b': np.max(self.errors_b),
        }
    
    def print_stats(self):
        """Print statistics to console"""
        stats = self.get_stats()
        if stats is None:
            print("No data collected yet")
            return
        
        print(f"\n{'=' * 60}")
        print(f"Performance Statistics (n={stats['count']})")
        print(f"{'=' * 60}")
        print(f"{'Channel':<10} {'Mean Error':<15} {'Max Error':<15}")
        print("-" * 60)
        print(f"{'Red':<10} {stats['mae_r']:>14.2f} {stats['max_error_r']:>14.2f}")
        print(f"{'Green':<10} {stats['mae_g']:>14.2f} {stats['max_error_g']:>14.2f}")
        print(f"{'Blue':<10} {stats['mae_b']:>14.2f} {stats['max_error_b']:>14.2f}")
        print(f"{'Average':<10} {(stats['mae_r'] + stats['mae_g'] + stats['mae_b'])/3:>14.2f}")
        print("=" * 60)


def get_key_nonblocking():
    """
    Non-blocking keyboard input
    Returns: character if key pressed, None otherwise
    """
    if IS_WINDOWS:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            try:
                return ch.decode(errors="ignore")
            except Exception:
                return None
        return None
    else:
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1)
        return None


# --- macOS / Linux terminal setup ---
if not IS_WINDOWS:
    fd = sys.stdin.fileno()
    old_term_attr = termios.tcgetattr(fd)
    tty.setcbreak(fd)


def test_env_module(env, index):
    """Test if Env module supports RGB"""
    print(f"\n{'=' * 60}")
    print(f"Env Module #{index + 1} (ID: 0x{env.id:X})")
    print(f"{'=' * 60}")
    print(f"App Version: {env.app_version}")

    if hasattr(env, '_is_rgb_supported') and env._is_rgb_supported():
        print("✓ RGB properties are supported!")
        return True
    else:
        print("✗ RGB properties are NOT supported in this version")
        return False


def main():
    """Main testing loop"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Real-time RGB model testing')
    parser.add_argument('--enhanced', action='store_true', 
                       help='Use enhanced model (rgb_models_enhanced.pkl) instead of basic model')
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("RGB MODEL REAL-TIME TESTING")
    if args.enhanced:
        print("Mode: ENHANCED (with feature engineering)")
    else:
        print("Mode: BASIC (raw features only)")
    print("=" * 60)
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Select model file
    if args.enhanced:
        model_path = os.path.join(script_dir, "rgb_models_enhanced.pkl")
    else:
        model_path = os.path.join(script_dir, "rgb_models.pkl")
    
    # Check if model file exists
    if not os.path.exists(model_path):
        print(f"\n✗ Error: Model file not found at {model_path}")
        if args.enhanced:
            print("Please run train_rgb_model_enhanced.py first to train the enhanced model.")
        else:
            print("Please run train_rgb_model.py first to train the basic model.")
        return
    
    # Load the trained model
    print(f"\nLoading trained model...")
    predictor = RGBModelPredictor(model_path, is_enhanced=args.enhanced)
    
    # Show model coefficients
    coeffs = predictor.get_coefficients()
    print(f"\nModel Coefficients:")
    for channel in ['r', 'g', 'b']:
        weights = coeffs[channel]['weights']
        bias = coeffs[channel]['bias']
        if predictor.is_enhanced:
            print(f"  {channel.upper()}: {len(weights)} features, bias={bias:.2f}")
        else:
            print(f"  {channel.upper()}: w={weights}, bias={bias:.2f}")
    
    # Initialize MODI+ connection
    print(f"\n{'=' * 60}")
    print("Connecting to MODI+ modules...")
    print(f"{'=' * 60}")
    
    bundle = modi_plus.MODIPlus()
    time.sleep(2)  # Wait for connection
    
    # Check for Env modules
    num_envs = len(bundle.envs)
    print(f"\nFound {num_envs} Env module(s)")
    
    if num_envs == 0:
        print("✗ Error: No Env modules found!")
        bundle.close()
        return
    
    # Test each Env module for RGB support
    rgb_supported_modules = []
    for i, env in enumerate(bundle.envs):
        if test_env_module(env, i):
            rgb_supported_modules.append((i, env))
    
    if not rgb_supported_modules:
        print("\n✗ No modules with RGB support found.")
        bundle.close()
        return
    
    # Start real-time testing
    print(f"\n{'=' * 60}")
    print(f"Real-time Testing with {len(rgb_supported_modules)} module(s)")
    print("=" * 60)
    print("\nOutput Format:")
    print("  RAW: R, G, B, W (4 values)")
    print("  RGB_255: R, G, B (3 values)")
    print("  RGB_100: R, G, B (3 values)")
    print("  Color: Classified color name (1 value)")
    print("  White_100: White component 0-100 scale (1 value)")
    print("  Black_100: Black component 0-100 scale (1 value)")
    print("  Total: 12 values per reading")
    print("\nColor Classification:")
    print("  Colors: Red, Green, Blue")
    print("  Achromatic: Black, White")
    print("  Unclear: Unknown")
    print("\nBlack/White Method: Color Theory")
    print("  White = min(R, G, B)")
    print("  Black = 255 - max(R, G, B)")
    print("\nCommands:")
    print("  - Press 's' to show statistics")
    print("  - Press 'r' to reset statistics")
    print("  - Press 'q' to quit")
    print(f"\n{'=' * 60}\n")
    
    time.sleep(2)
    
    # Performance tracker for each module
    trackers: Dict[int, PerformanceTracker] = {}
    for idx, _ in rgb_supported_modules:
        trackers[idx] = PerformanceTracker()
    
    try:
        while True:
            # Check for keyboard input
            ch = get_key_nonblocking()
            if ch is not None:
                ch_lower = ch.lower()
                if ch_lower == 'q':
                    print("\n\nExiting...")
                    break
                elif ch_lower == 's':
                    print("\n\n" + "=" * 60)
                    print("STATISTICS")
                    print("=" * 60)
                    for idx in sorted(trackers.keys()):
                        print(f"\nModule #{idx + 1}:")
                        trackers[idx].print_stats()
                    print("\nPress any key to continue...\n")
                    time.sleep(2)
                elif ch_lower == 'r':
                    for tracker in trackers.values():
                        tracker.reset()
                    print("\n\n✓ Statistics reset\n")
                    time.sleep(1)
            
            # Read and process data from all modules
            display_lines = []
            
            for idx, env in rgb_supported_modules:
                try:
                    # Set RGB mode
                    env.set_rgb_mode(env.RGB_MODE_ON, 300)
                    
                    # Read sensor values
                    raw_r, raw_g, raw_b, raw_w = env.raw_rgb
                    
                    # Predict using model
                    pred_r, pred_g, pred_b = predictor.predict(raw_r, raw_g, raw_b, raw_w)
                    
                    # Convert to RGB 100 scale
                    pred_r_100, pred_g_100, pred_b_100 = RGBConverter.rgb_255_to_100(pred_r, pred_g, pred_b)
                    
                    # Calculate Black/White using Method 1 (Color Theory)
                    white, black = RGBConverter.calculate_black_white_method1(pred_r, pred_g, pred_b)
                    
                    # Convert White/Black to 0-100 scale
                    white_100 = int(round(white * 100 / 255))
                    black_100 = int(round(black * 100 / 255))
                    
                    # Classify color based on RGB and White/Black
                    color_name = RGBConverter.classify_color(pred_r, pred_g, pred_b, white, black)
                    
                    # Format output line (12 values total)
                    line = f"M#{idx + 1}: "
                    line += f"RAW({raw_r:4d},{raw_g:4d},{raw_b:4d},{raw_w:4d}) | "
                    line += f"255({pred_r:3d},{pred_g:3d},{pred_b:3d}) | "
                    line += f"100({pred_r_100:2d},{pred_g_100:2d},{pred_b_100:2d}) | "
                    line += f"Color:{color_name:10s} W:{white_100:2d} K:{black_100:2d}"
                    
                    display_lines.append(line)
                    
                except Exception as e:
                    display_lines.append(f"M#{idx + 1}: Error - {e}")
            
            # Display
            if len(display_lines) == 1:
                # Single module - overwrite same line
                print(display_lines[0] + " " * 20, end="\r", flush=True)
            else:
                # Multiple modules
                output = "\n".join(display_lines)
                print(output + "\n", end="", flush=True)
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\nStopped by user (Ctrl+C)")
    
    finally:
        # Print final statistics
        print("\n\n" + "=" * 60)
        print("FINAL STATISTICS")
        print("=" * 60)
        for idx in sorted(trackers.keys()):
            print(f"\nModule #{idx + 1}:")
            trackers[idx].print_stats()
        
        # Cleanup
        if not IS_WINDOWS:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_term_attr)
        
        bundle.close()
        print("\n✓ Connection closed")
        print("=" * 60)


if __name__ == "__main__":
    main()

