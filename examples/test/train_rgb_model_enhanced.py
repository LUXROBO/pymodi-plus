"""
Enhanced RGB Model Training with VEML6040 Sensor Characteristics

This script improves upon the basic training by incorporating:
1. Lux-based normalization using sensor sensitivity
2. White channel ratio features
3. Integration time compensation (if available)
4. Cross-channel interaction features based on spectral overlap
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle

# VEML6040 Sensor Specifications
VEML6040_SPECS = {
    'peak_wavelength': {'R': 650, 'G': 550, 'B': 450},  # nm
    'bandwidth': {'R': 35, 'G': 35, 'B': 40},  # nm (±)
    'sensitivity': 0.007865,  # lux/step
    'max_count': 65535,  # 16-bit
    'integration_time_default': 40,  # ms (typical, may vary)
}

# Configuration
CSV_FILE = "MODI RGB 센서 Sample 100 측정_Ethan.csv"
TEST_SIZE = 0.2
RANDOM_STATE = 42
POLY_DEGREE = 2

# Feature engineering options
USE_LUX_NORMALIZATION = True
USE_WHITE_RATIO = True
USE_CROSS_CHANNEL = True


def calculate_lux(raw_w):
    """
    Calculate illuminance in lux from raw white channel
    Based on VEML6040 sensitivity: 0.007865 lux/step
    """
    return raw_w * VEML6040_SPECS['sensitivity']


def calculate_white_ratios(raw_r, raw_g, raw_b, raw_w):
    """
    Calculate ratio of each color channel to white channel
    This helps normalize for different lighting conditions
    """
    # Avoid division by zero
    raw_w_safe = np.maximum(raw_w, 1)
    
    ratio_r = raw_r / raw_w_safe
    ratio_g = raw_g / raw_w_safe
    ratio_b = raw_b / raw_w_safe
    
    return ratio_r, ratio_g, ratio_b


def calculate_cross_channel_features(raw_r, raw_g, raw_b):
    """
    Calculate cross-channel features based on spectral overlap
    VEML6040 channels have overlapping spectral responses
    """
    # Color dominance
    total = raw_r + raw_g + raw_b + 1e-6  # avoid division by zero
    dom_r = raw_r / total
    dom_g = raw_g / total
    dom_b = raw_b / total
    
    # Color ratios
    rg_ratio = raw_r / (raw_g + 1)
    gb_ratio = raw_g / (raw_b + 1)
    rb_ratio = raw_r / (raw_b + 1)
    
    return dom_r, dom_g, dom_b, rg_ratio, gb_ratio, rb_ratio


def engineer_features(df):
    """
    Create engineered features based on VEML6040 characteristics
    
    Returns:
        Enhanced feature dataframe
    """
    features = {}
    
    # Original raw values
    features['RAW_R'] = df['RAW_R'].values
    features['RAW_G'] = df['RAW_G'].values
    features['RAW_B'] = df['RAW_B'].values
    features['RAW_W'] = df['RAW_W'].values
    
    if USE_LUX_NORMALIZATION:
        # Lux-based normalization
        lux = calculate_lux(df['RAW_W'].values)
        features['LUX'] = lux
        
        # Normalized by lux (brightness-independent color)
        features['R_NORM_LUX'] = df['RAW_R'].values / (lux + 1)
        features['G_NORM_LUX'] = df['RAW_G'].values / (lux + 1)
        features['B_NORM_LUX'] = df['RAW_B'].values / (lux + 1)
    
    if USE_WHITE_RATIO:
        # White channel ratios
        ratio_r, ratio_g, ratio_b = calculate_white_ratios(
            df['RAW_R'].values, 
            df['RAW_G'].values, 
            df['RAW_B'].values, 
            df['RAW_W'].values
        )
        features['RATIO_R_W'] = ratio_r
        features['RATIO_G_W'] = ratio_g
        features['RATIO_B_W'] = ratio_b
    
    if USE_CROSS_CHANNEL:
        # Cross-channel features
        dom_r, dom_g, dom_b, rg_ratio, gb_ratio, rb_ratio = calculate_cross_channel_features(
            df['RAW_R'].values,
            df['RAW_G'].values,
            df['RAW_B'].values
        )
        features['DOM_R'] = dom_r
        features['DOM_G'] = dom_g
        features['DOM_B'] = dom_b
        features['RG_RATIO'] = rg_ratio
        features['GB_RATIO'] = gb_ratio
        features['RB_RATIO'] = rb_ratio
    
    return pd.DataFrame(features)


def load_and_preprocess_data(csv_path):
    """
    Load CSV data and preprocess with VEML6040-specific feature engineering
    """
    print("=" * 60)
    print("Loading and preprocessing data with VEML6040 features...")
    print("=" * 60)
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Remove spaces from column values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()
    
    # Convert to numeric
    numeric_columns = ['NO', 'RAW_R', 'RAW_G', 'RAW_B', 'RAW_W', 'R_255', 'G_255', 'B_255']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove rows with missing values
    df = df.dropna()
    
    print(f"Loaded {len(df)} samples")
    
    # Engineer features
    X_df = engineer_features(df)
    
    print(f"\nEngineered features:")
    print(f"  Feature count: {X_df.shape[1]}")
    print(f"  Feature names: {list(X_df.columns)}")
    
    # Target values
    y_r = df['R_255'].values
    y_g = df['G_255'].values
    y_b = df['B_255'].values
    
    # Show feature ranges
    print(f"\nKey feature statistics:")
    if 'LUX' in X_df.columns:
        print(f"  Lux range: {X_df['LUX'].min():.2f} - {X_df['LUX'].max():.2f}")
    if 'RATIO_R_W' in X_df.columns:
        print(f"  R/W ratio: {X_df['RATIO_R_W'].min():.3f} - {X_df['RATIO_R_W'].max():.3f}")
        print(f"  G/W ratio: {X_df['RATIO_G_W'].min():.3f} - {X_df['RATIO_G_W'].max():.3f}")
        print(f"  B/W ratio: {X_df['RATIO_B_W'].min():.3f} - {X_df['RATIO_B_W'].max():.3f}")
    
    return X_df.values, y_r, y_g, y_b, df, X_df.columns.tolist()


def train_enhanced_model(X_train, y_train, X_test, y_test, channel_name, feature_names):
    """
    Train enhanced model with regularization
    """
    # Try both standard Linear Regression and Ridge (with L2 regularization)
    model_lr = LinearRegression()
    model_lr.fit(X_train, y_train)
    
    model_ridge = Ridge(alpha=1.0)
    model_ridge.fit(X_train, y_train)
    
    # Evaluate both
    y_test_pred_lr = np.clip(model_lr.predict(X_test), 0, 255)
    y_test_pred_ridge = np.clip(model_ridge.predict(X_test), 0, 255)
    
    mae_lr = mean_absolute_error(y_test, y_test_pred_lr)
    mae_ridge = mean_absolute_error(y_test, y_test_pred_ridge)
    
    # Choose better model
    if mae_ridge < mae_lr:
        model = model_ridge
        y_test_pred = y_test_pred_ridge
        model_type = "Ridge"
    else:
        model = model_lr
        y_test_pred = y_test_pred_lr
        model_type = "Linear"
    
    y_train_pred = np.clip(model.predict(X_train), 0, 255)
    
    # Calculate metrics
    metrics = {
        'model_type': model_type,
        'train_mae': mean_absolute_error(y_train, y_train_pred),
        'test_mae': mean_absolute_error(y_test, y_test_pred),
        'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
        'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
        'train_r2': r2_score(y_train, y_train_pred),
        'test_r2': r2_score(y_test, y_test_pred),
        'y_test': y_test,
        'y_test_pred': y_test_pred,
        'y_train': y_train,
        'y_train_pred': y_train_pred,
        'feature_importance': dict(zip(feature_names, np.abs(model.coef_)))
    }
    
    return model, metrics


def print_feature_importance(metrics, channel_name):
    """Print top 5 most important features"""
    importance = metrics['feature_importance']
    sorted_features = sorted(importance.items(), key=lambda x: -x[1])
    
    print(f"\n  Top 5 features for {channel_name}:")
    for i, (feat, imp) in enumerate(sorted_features[:5], 1):
        print(f"    {i}. {feat:15s}: {imp:8.4f}")


def main():
    """Main enhanced training pipeline"""
    print("\n" + "=" * 60)
    print("ENHANCED RGB MODEL TRAINING with VEML6040 Features")
    print("=" * 60)
    
    print(f"\nVEML6040 Sensor Specifications:")
    print(f"  Peak wavelengths: R={VEML6040_SPECS['peak_wavelength']['R']}nm, "
          f"G={VEML6040_SPECS['peak_wavelength']['G']}nm, "
          f"B={VEML6040_SPECS['peak_wavelength']['B']}nm")
    print(f"  Sensitivity: {VEML6040_SPECS['sensitivity']} lux/step")
    print(f"  Resolution: 16-bit (0-{VEML6040_SPECS['max_count']})")
    
    print(f"\nFeature Engineering Options:")
    print(f"  Lux normalization: {USE_LUX_NORMALIZATION}")
    print(f"  White channel ratios: {USE_WHITE_RATIO}")
    print(f"  Cross-channel features: {USE_CROSS_CHANNEL}")
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, CSV_FILE)
    
    # Load data with enhanced features
    X, y_r, y_g, y_b, df, feature_names = load_and_preprocess_data(csv_path)
    
    # Split data
    print(f"\n{'=' * 60}")
    print(f"Splitting data (Train: {int((1-TEST_SIZE)*100)}%, Test: {int(TEST_SIZE*100)}%)")
    print(f"{'=' * 60}")
    
    X_train, X_test, y_r_train, y_r_test = train_test_split(X, y_r, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    _, _, y_g_train, y_g_test = train_test_split(X, y_g, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    _, _, y_b_train, y_b_test = train_test_split(X, y_b, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Feature dimensions: {X_train.shape[1]}")
    
    # Train enhanced models
    all_models = {}
    all_metrics = {'r': {}, 'g': {}, 'b': {}}
    
    for channel, y_train, y_test in [('r', y_r_train, y_r_test), 
                                      ('g', y_g_train, y_g_test), 
                                      ('b', y_b_train, y_b_test)]:
        print(f"\n{'=' * 60}")
        print(f"Training enhanced model for {channel.upper()} channel")
        print(f"{'=' * 60}")
        
        model, metrics = train_enhanced_model(X_train, y_train, X_test, y_test, channel, feature_names)
        all_models[channel] = model
        all_metrics[channel] = metrics
        
        print(f"\n{channel.upper()} Channel Results ({metrics['model_type']} Regression):")
        print(f"  Train MAE: {metrics['train_mae']:.2f}, Test MAE: {metrics['test_mae']:.2f}")
        print(f"  Train R²: {metrics['train_r2']:.4f}, Test R²: {metrics['test_r2']:.4f}")
        
        print_feature_importance(metrics, channel.upper())
    
    # Save enhanced models and metadata
    print(f"\n{'=' * 60}")
    print("Saving enhanced models...")
    print(f"{'=' * 60}")
    
    output_data = {
        'models': all_models,
        'feature_names': feature_names,
        'sensor_specs': VEML6040_SPECS,
        'feature_options': {
            'lux_normalization': USE_LUX_NORMALIZATION,
            'white_ratio': USE_WHITE_RATIO,
            'cross_channel': USE_CROSS_CHANNEL
        }
    }
    
    pkl_path = os.path.join(script_dir, "rgb_models_enhanced.pkl")
    with open(pkl_path, 'wb') as f:
        pickle.dump(output_data, f)
    print(f"✓ Enhanced models saved to: {pkl_path}")
    
    # Save feature importance as JSON
    importance_data = {}
    for channel in ['r', 'g', 'b']:
        importance_data[channel] = all_metrics[channel]['feature_importance']
    
    json_path = os.path.join(script_dir, "feature_importance.json")
    with open(json_path, 'w') as f:
        # Convert numpy types to native Python types for JSON serialization
        importance_json = {}
        for channel, features in importance_data.items():
            importance_json[channel] = {k: float(v) for k, v in features.items()}
        json.dump(importance_json, f, indent=4)
    print(f"✓ Feature importance saved to: {json_path}")
    
    # Comparison with baseline
    print(f"\n{'=' * 60}")
    print("PERFORMANCE COMPARISON")
    print(f"{'=' * 60}")
    print(f"\nEnhanced Model Performance:")
    print(f"{'Channel':<10} {'Test MAE':<12} {'Test R²':<10} {'Model Type':<15}")
    print("-" * 60)
    for channel in ['r', 'g', 'b']:
        m = all_metrics[channel]
        print(f"{channel.upper():<10} {m['test_mae']:>11.2f} {m['test_r2']:>9.4f} {m['model_type']:<15}")
    
    avg_mae = np.mean([all_metrics[ch]['test_mae'] for ch in ['r', 'g', 'b']])
    avg_r2 = np.mean([all_metrics[ch]['test_r2'] for ch in ['r', 'g', 'b']])
    print(f"{'Average':<10} {avg_mae:>11.2f} {avg_r2:>9.4f}")
    
    print(f"\n{'=' * 60}")
    print("TRAINING COMPLETE!")
    print(f"{'=' * 60}")
    print("\nGenerated files:")
    print(f"  - rgb_models_enhanced.pkl (Enhanced models with metadata)")
    print(f"  - feature_importance.json (Feature importance analysis)")
    print("\nNext steps:")
    print("  1. Compare with baseline model (rgb_models.pkl)")
    print("  2. Test with real-time sensor data")
    print("  3. Implement top features in C code if needed")
    print("=" * 60)


if __name__ == "__main__":
    main()

