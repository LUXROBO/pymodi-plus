"""
RGB Sensor Calibration Model Training Script

This script trains machine learning models to predict actual RGB values (0-255)
from raw sensor readings (RAW_R, RAW_G, RAW_B, RAW_W).

The trained model coefficients are exported in C-compatible format for 
embedded system implementation.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle

# Configuration
CSV_FILE = "MODI RGB 센서 Sample 100 측정_Ethan.csv"
TEST_SIZE = 0.2
RANDOM_STATE = 42
POLY_DEGREE = 2

def load_and_preprocess_data(csv_path):
    """
    Load CSV data and preprocess (remove spaces, handle missing values)
    
    Returns:
        X: Input features (RAW_R, RAW_G, RAW_B, RAW_W)
        y: Target values (R_255, G_255, B_255)
        df: Original dataframe for reference
    """
    print("=" * 60)
    print("Loading and preprocessing data...")
    print("=" * 60)
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Remove spaces from column values (they have trailing spaces)
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
    print(f"\nData shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    # Prepare features (X) and targets (y)
    X = df[['RAW_R', 'RAW_G', 'RAW_B', 'RAW_W']].values
    y_r = df['R_255'].values
    y_g = df['G_255'].values
    y_b = df['B_255'].values
    
    print(f"\nFeature ranges:")
    print(f"  RAW_R: {X[:, 0].min():.0f} - {X[:, 0].max():.0f}")
    print(f"  RAW_G: {X[:, 1].min():.0f} - {X[:, 1].max():.0f}")
    print(f"  RAW_B: {X[:, 2].min():.0f} - {X[:, 2].max():.0f}")
    print(f"  RAW_W: {X[:, 3].min():.0f} - {X[:, 3].max():.0f}")
    
    print(f"\nTarget ranges:")
    print(f"  R_255: {y_r.min():.0f} - {y_r.max():.0f}")
    print(f"  G_255: {y_g.min():.0f} - {y_g.max():.0f}")
    print(f"  B_255: {y_b.min():.0f} - {y_b.max():.0f}")
    
    return X, y_r, y_g, y_b, df


def train_linear_model(X_train, y_train, X_test, y_test, channel_name):
    """
    Train a linear regression model
    
    Returns:
        model: Trained model
        metrics: Dictionary of performance metrics
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Clip predictions to valid range [0, 255]
    y_train_pred = np.clip(y_train_pred, 0, 255)
    y_test_pred = np.clip(y_test_pred, 0, 255)
    
    # Calculate metrics
    metrics = {
        'train_mae': mean_absolute_error(y_train, y_train_pred),
        'test_mae': mean_absolute_error(y_test, y_test_pred),
        'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
        'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
        'train_r2': r2_score(y_train, y_train_pred),
        'test_r2': r2_score(y_test, y_test_pred),
        'y_test': y_test,
        'y_test_pred': y_test_pred,
        'y_train': y_train,
        'y_train_pred': y_train_pred
    }
    
    return model, metrics


def train_polynomial_model(X_train, y_train, X_test, y_test, channel_name, degree=2):
    """
    Train a polynomial regression model
    
    Returns:
        model: Trained model
        poly: PolynomialFeatures transformer
        metrics: Dictionary of performance metrics
    """
    poly = PolynomialFeatures(degree=degree, include_bias=True)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)
    
    model = LinearRegression()
    model.fit(X_train_poly, y_train)
    
    # Predictions
    y_train_pred = model.predict(X_train_poly)
    y_test_pred = model.predict(X_test_poly)
    
    # Clip predictions to valid range [0, 255]
    y_train_pred = np.clip(y_train_pred, 0, 255)
    y_test_pred = np.clip(y_test_pred, 0, 255)
    
    # Calculate metrics
    metrics = {
        'train_mae': mean_absolute_error(y_train, y_train_pred),
        'test_mae': mean_absolute_error(y_test, y_test_pred),
        'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
        'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
        'train_r2': r2_score(y_train, y_train_pred),
        'test_r2': r2_score(y_test, y_test_pred),
        'y_test': y_test,
        'y_test_pred': y_test_pred,
        'y_train': y_train,
        'y_train_pred': y_train_pred
    }
    
    return model, poly, metrics


def print_model_evaluation(channel_name, linear_metrics, poly_metrics):
    """Print model evaluation results"""
    print(f"\n{'=' * 60}")
    print(f"Channel: {channel_name}")
    print(f"{'=' * 60}")
    
    print(f"\n{'Model':<20} {'Train MAE':<12} {'Test MAE':<12} {'Train RMSE':<12} {'Test RMSE':<12} {'Train R²':<10} {'Test R²':<10}")
    print("-" * 100)
    
    print(f"{'Linear Regression':<20} {linear_metrics['train_mae']:>11.2f} {linear_metrics['test_mae']:>11.2f} "
          f"{linear_metrics['train_rmse']:>11.2f} {linear_metrics['test_rmse']:>11.2f} "
          f"{linear_metrics['train_r2']:>9.4f} {linear_metrics['test_r2']:>9.4f}")
    
    print(f"{'Polynomial (deg=2)':<20} {poly_metrics['train_mae']:>11.2f} {poly_metrics['test_mae']:>11.2f} "
          f"{poly_metrics['train_rmse']:>11.2f} {poly_metrics['test_rmse']:>11.2f} "
          f"{poly_metrics['train_r2']:>9.4f} {poly_metrics['test_r2']:>9.4f}")
    
    # Overfitting check
    linear_overfit = linear_metrics['train_r2'] - linear_metrics['test_r2']
    poly_overfit = poly_metrics['train_r2'] - poly_metrics['test_r2']
    
    print(f"\nOverfitting check (Train R² - Test R²):")
    print(f"  Linear: {linear_overfit:+.4f}")
    print(f"  Polynomial: {poly_overfit:+.4f}")
    
    if poly_metrics['test_mae'] < linear_metrics['test_mae']:
        print(f"\n✓ Polynomial model performs better (lower test MAE)")
    else:
        print(f"\n✓ Linear model performs better (lower test MAE)")


def export_coefficients_to_c(models, output_dir="."):
    """
    Export model coefficients to C header file and JSON
    
    Args:
        models: Dictionary with keys 'r', 'g', 'b' containing trained models
        output_dir: Directory to save output files
    """
    print(f"\n{'=' * 60}")
    print("Exporting coefficients for C implementation")
    print(f"{'=' * 60}")
    
    # Prepare data structures
    coefficients = {}
    
    for channel, model in models.items():
        weights = model.coef_
        bias = model.intercept_
        
        coefficients[channel] = {
            'weights': weights.tolist(),
            'bias': float(bias)
        }
        
        print(f"\n{channel.upper()} channel:")
        print(f"  Weights: {weights}")
        print(f"  Bias: {bias:.6f}")
        print(f"  Equation: {channel.upper()} = {weights[0]:.6f}*RAW_R + {weights[1]:.6f}*RAW_G + {weights[2]:.6f}*RAW_B + {weights[3]:.6f}*RAW_W + {bias:.6f}")
    
    # Save as JSON
    json_path = os.path.join(output_dir, "rgb_model_coefficients.json")
    with open(json_path, 'w') as f:
        json.dump(coefficients, f, indent=4)
    print(f"\n✓ JSON coefficients saved to: {json_path}")
    
    # Generate C header file
    h_path = os.path.join(output_dir, "rgb_model_coefficients.h")
    with open(h_path, 'w') as f:
        f.write("/* Auto-generated RGB sensor calibration coefficients */\n")
        f.write("/* Generated from train_rgb_model.py */\n\n")
        f.write("#ifndef RGB_MODEL_COEFFICIENTS_H\n")
        f.write("#define RGB_MODEL_COEFFICIENTS_H\n\n")
        
        for channel in ['r', 'g', 'b']:
            weights = coefficients[channel]['weights']
            bias = coefficients[channel]['bias']
            
            f.write(f"/* {channel.upper()} channel coefficients */\n")
            f.write(f"const float weights_{channel}[4] = {{\n")
            f.write(f"    {weights[0]:.10f}f,  /* RAW_R coefficient */\n")
            f.write(f"    {weights[1]:.10f}f,  /* RAW_G coefficient */\n")
            f.write(f"    {weights[2]:.10f}f,  /* RAW_B coefficient */\n")
            f.write(f"    {weights[3]:.10f}f   /* RAW_W coefficient */\n")
            f.write(f"}};\n")
            f.write(f"const float bias_{channel} = {bias:.10f}f;\n\n")
        
        # Add prediction functions
        f.write("/* Prediction functions */\n")
        for channel in ['r', 'g', 'b']:
            f.write(f"static inline float predict_{channel}(float raw_r, float raw_g, float raw_b, float raw_w) {{\n")
            f.write(f"    float result = weights_{channel}[0] * raw_r + \n")
            f.write(f"                   weights_{channel}[1] * raw_g + \n")
            f.write(f"                   weights_{channel}[2] * raw_b + \n")
            f.write(f"                   weights_{channel}[3] * raw_w + \n")
            f.write(f"                   bias_{channel};\n")
            f.write(f"    \n")
            f.write(f"    /* Clip to valid range [0, 255] */\n")
            f.write(f"    if (result < 0.0f) result = 0.0f;\n")
            f.write(f"    if (result > 255.0f) result = 255.0f;\n")
            f.write(f"    \n")
            f.write(f"    return result;\n")
            f.write(f"}}\n\n")
        
        f.write("#endif /* RGB_MODEL_COEFFICIENTS_H */\n")
    
    print(f"✓ C header file saved to: {h_path}")
    
    # Save models as pickle for Python use
    pkl_path = os.path.join(output_dir, "rgb_models.pkl")
    with open(pkl_path, 'wb') as f:
        pickle.dump(models, f)
    print(f"✓ Pickle models saved to: {pkl_path}")


def plot_results(models_dict, X_test, metrics_dict, output_dir="."):
    """
    Create visualization plots for model performance
    
    Args:
        models_dict: Dictionary with 'linear' and 'poly' models for each channel
        X_test: Test features
        metrics_dict: Dictionary with metrics for each model
        output_dir: Directory to save plots
    """
    print(f"\n{'=' * 60}")
    print("Generating visualization plots...")
    print(f"{'=' * 60}")
    
    # Create figure with subplots
    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    fig.suptitle('RGB Sensor Calibration Model Performance', fontsize=16, fontweight='bold')
    
    channels = ['r', 'g', 'b']
    channel_names = ['Red', 'Green', 'Blue']
    colors = ['red', 'green', 'blue']
    
    for idx, (channel, channel_name, color) in enumerate(zip(channels, channel_names, colors)):
        # Linear model plot
        ax_linear = axes[idx, 0]
        linear_metrics = metrics_dict[channel]['linear']
        
        ax_linear.scatter(linear_metrics['y_test'], linear_metrics['y_test_pred'], 
                         alpha=0.6, c=color, s=50, edgecolors='black', linewidth=0.5)
        
        # Perfect prediction line
        min_val = min(linear_metrics['y_test'].min(), linear_metrics['y_test_pred'].min())
        max_val = max(linear_metrics['y_test'].max(), linear_metrics['y_test_pred'].max())
        ax_linear.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=2, label='Perfect prediction')
        
        ax_linear.set_xlabel('Actual Value', fontsize=11)
        ax_linear.set_ylabel('Predicted Value', fontsize=11)
        ax_linear.set_title(f'{channel_name} - Linear Regression\n'
                           f'MAE={linear_metrics["test_mae"]:.2f}, R²={linear_metrics["test_r2"]:.4f}', 
                           fontsize=12)
        ax_linear.legend()
        ax_linear.grid(True, alpha=0.3)
        
        # Polynomial model plot
        ax_poly = axes[idx, 1]
        poly_metrics = metrics_dict[channel]['poly']
        
        ax_poly.scatter(poly_metrics['y_test'], poly_metrics['y_test_pred'], 
                       alpha=0.6, c=color, s=50, edgecolors='black', linewidth=0.5)
        
        # Perfect prediction line
        min_val = min(poly_metrics['y_test'].min(), poly_metrics['y_test_pred'].min())
        max_val = max(poly_metrics['y_test'].max(), poly_metrics['y_test_pred'].max())
        ax_poly.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=2, label='Perfect prediction')
        
        ax_poly.set_xlabel('Actual Value', fontsize=11)
        ax_poly.set_ylabel('Predicted Value', fontsize=11)
        ax_poly.set_title(f'{channel_name} - Polynomial Regression (degree=2)\n'
                         f'MAE={poly_metrics["test_mae"]:.2f}, R²={poly_metrics["test_r2"]:.4f}', 
                         fontsize=12)
        ax_poly.legend()
        ax_poly.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "model_performance.png")
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"✓ Plot saved to: {plot_path}")
    
    # Create residual plots
    fig_res, axes_res = plt.subplots(1, 3, figsize=(15, 4))
    fig_res.suptitle('Residual Analysis (Linear Models)', fontsize=16, fontweight='bold')
    
    for idx, (channel, channel_name, color) in enumerate(zip(channels, channel_names, colors)):
        ax = axes_res[idx]
        linear_metrics = metrics_dict[channel]['linear']
        
        residuals = linear_metrics['y_test'] - linear_metrics['y_test_pred']
        
        ax.scatter(linear_metrics['y_test_pred'], residuals, 
                  alpha=0.6, c=color, s=50, edgecolors='black', linewidth=0.5)
        ax.axhline(y=0, color='k', linestyle='--', linewidth=2)
        ax.set_xlabel('Predicted Value', fontsize=11)
        ax.set_ylabel('Residual (Actual - Predicted)', fontsize=11)
        ax.set_title(f'{channel_name} Channel', fontsize=12)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    residual_path = os.path.join(output_dir, "residual_analysis.png")
    plt.savefig(residual_path, dpi=150, bbox_inches='tight')
    print(f"✓ Residual plot saved to: {residual_path}")
    
    plt.show()


def main():
    """Main training pipeline"""
    print("\n" + "=" * 60)
    print("RGB SENSOR CALIBRATION MODEL TRAINING")
    print("=" * 60)
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, CSV_FILE)
    
    # Load data
    X, y_r, y_g, y_b, df = load_and_preprocess_data(csv_path)
    
    # Split data
    print(f"\n{'=' * 60}")
    print(f"Splitting data (Train: {int((1-TEST_SIZE)*100)}%, Test: {int(TEST_SIZE*100)}%)")
    print(f"{'=' * 60}")
    
    X_train, X_test, y_r_train, y_r_test = train_test_split(X, y_r, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    _, _, y_g_train, y_g_test = train_test_split(X, y_g, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    _, _, y_b_train, y_b_test = train_test_split(X, y_b, test_size=TEST_SIZE, random_state=RANDOM_STATE)
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train models for each channel
    all_linear_models = {}
    all_poly_models = {}
    all_poly_transformers = {}
    all_metrics = {'r': {}, 'g': {}, 'b': {}}
    
    for channel, y_train, y_test in [('r', y_r_train, y_r_test), 
                                      ('g', y_g_train, y_g_test), 
                                      ('b', y_b_train, y_b_test)]:
        print(f"\n{'=' * 60}")
        print(f"Training models for {channel.upper()} channel")
        print(f"{'=' * 60}")
        
        # Train linear model
        linear_model, linear_metrics = train_linear_model(X_train, y_train, X_test, y_test, channel)
        all_linear_models[channel] = linear_model
        all_metrics[channel]['linear'] = linear_metrics
        
        # Train polynomial model
        poly_model, poly_transformer, poly_metrics = train_polynomial_model(
            X_train, y_train, X_test, y_test, channel, degree=POLY_DEGREE
        )
        all_poly_models[channel] = poly_model
        all_poly_transformers[channel] = poly_transformer
        all_metrics[channel]['poly'] = poly_metrics
        
        # Print evaluation
        print_model_evaluation(channel.upper(), linear_metrics, poly_metrics)
    
    # Export coefficients (using linear models for C implementation)
    export_coefficients_to_c(all_linear_models, output_dir=script_dir)
    
    # Create visualizations
    plot_results(
        {'linear': all_linear_models, 'poly': all_poly_models},
        X_test,
        all_metrics,
        output_dir=script_dir
    )
    
    print(f"\n{'=' * 60}")
    print("TRAINING COMPLETE!")
    print(f"{'=' * 60}")
    print("\nGenerated files:")
    print(f"  - rgb_model_coefficients.h (C header file)")
    print(f"  - rgb_model_coefficients.json (JSON format)")
    print(f"  - rgb_models.pkl (Python pickle)")
    print(f"  - model_performance.png (Performance plots)")
    print(f"  - residual_analysis.png (Residual plots)")
    print("\nNext steps:")
    print("  1. Review the model performance metrics and plots")
    print("  2. Use the .h file to implement predictions in C code")
    print("  3. Test the model with new sensor data")
    print("=" * 60)


if __name__ == "__main__":
    main()

