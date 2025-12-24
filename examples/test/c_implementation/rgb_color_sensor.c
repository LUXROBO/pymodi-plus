/**
 * RGB Color Sensor Calibration and Classification - C Implementation
 * 
 * Based on trained machine learning model from train_rgb_model.py
 * Uses Color Theory method for White/Black calculation
 */

#include <stdint.h>
#include <math.h>

// RGB 색상 분류
typedef enum RGB_color_type_t {
    COLOR_UNKNOWN = 0,
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_WHITE,
    COLOR_BLACK,
} RGB_color_type_t;

// RGB 값
struct RGB_color_data_t {
    uint16_t r_raw;         // RAW RED 값
    uint16_t g_raw;         // RAW GREEN 값
    uint16_t b_raw;         // RAW BLUE 값
    uint16_t w_raw;         // RAW WHITE 값
    uint8_t red;            // 0~100% RED 신뢰도
    uint8_t green;          // 0~100% GREEN 신뢰도
    uint8_t blue;           // 0~100% BLUE 신뢰도
    uint8_t white;          // 0~100% WHITE 신뢰도
    uint8_t black;          // 0~100% BLACK 신뢰도
    uint8_t color;          // RGB_color_type_t (최종 판별 색상)
    uint8_t brightness;     // X 구현 X
};

// Model coefficients from training (rgb_model_coefficients.h)
// These values should be replaced with actual trained model coefficients
typedef struct {
    float weights[4];  // [RAW_R, RAW_G, RAW_B, RAW_W]
    float bias;
} LinearModel;

// Basic model coefficients (example - replace with actual values from training)
static const LinearModel MODEL_R = {
    .weights = {-0.004608f, -0.145180f, -0.106623f, 0.182864f},
    .bias = 27.825129f
};

static const LinearModel MODEL_G = {
    .weights = {0.058051f, 0.198650f, 0.003737f, -0.110795f},
    .bias = 66.999206f
};

static const LinearModel MODEL_B = {
    .weights = {-0.037995f, -0.070122f, 0.254771f, 0.014841f},
    .bias = 49.943655f
};

/**
 * Predict RGB value using linear model
 */
static float predict_channel(uint16_t r_raw, uint16_t g_raw, uint16_t b_raw, uint16_t w_raw, 
                              const LinearModel *model) {
    float result = model->weights[0] * r_raw + 
                   model->weights[1] * g_raw + 
                   model->weights[2] * b_raw + 
                   model->weights[3] * w_raw + 
                   model->bias;
    
    // Clip to valid range [0, 255]
    if (result < 0.0f) result = 0.0f;
    if (result > 255.0f) result = 255.0f;
    
    return result;
}

/**
 * Convert 0-255 scale to 0-100 scale
 */
static uint8_t scale_255_to_100(float value_255) {
    float value_100 = (value_255 * 100.0f / 255.0f) + 0.5f;  // +0.5 for rounding
    
    if (value_100 < 0.0f) return 0;
    if (value_100 > 100.0f) return 100;
    
    return (uint8_t)value_100;
}

/**
 * Find minimum of three values
 */
static float min3(float a, float b, float c) {
    float min = a;
    if (b < min) min = b;
    if (c < min) min = c;
    return min;
}

/**
 * Find maximum of three values
 */
static float max3(float a, float b, float c) {
    float max = a;
    if (b > max) max = b;
    if (c > max) max = c;
    return max;
}

/**
 * Calculate White and Black components using Color Theory
 * White = min(R, G, B)
 * Black = 255 - max(R, G, B)
 */
static void calculate_white_black(float r_255, float g_255, float b_255, 
                                   uint8_t *white_100, uint8_t *black_100) {
    // Color Theory method
    float white_255 = min3(r_255, g_255, b_255);
    float black_255 = 255.0f - max3(r_255, g_255, b_255);
    
    // Convert to 0-100 scale
    *white_100 = scale_255_to_100(white_255);
    *black_100 = scale_255_to_100(black_255);
}

/**
 * Classify color based on RGB values
 * Returns: COLOR_RED, COLOR_GREEN, COLOR_BLUE, COLOR_WHITE, COLOR_BLACK, or COLOR_UNKNOWN
 */
static RGB_color_type_t classify_color(float r_255, float g_255, float b_255) {
    const float THRESHOLD = 50.0f;  // Minimum difference for dominant color
    
    float max_rgb = max3(r_255, g_255, b_255);
    float min_rgb = min3(r_255, g_255, b_255);
    
    // Very dark -> Black
    if (max_rgb < 40.0f) {
        return COLOR_BLACK;
    }
    
    // Very bright and low saturation -> White
    if (min_rgb > 180.0f && (max_rgb - min_rgb) < 50.0f) {
        return COLOR_WHITE;
    }
    
    // Signal too weak -> Unknown
    if (max_rgb < 60.0f) {
        return COLOR_UNKNOWN;
    }
    
    // Find dominant color
    if (r_255 > g_255 && r_255 > b_255) {
        // Red is dominant
        if (r_255 > (g_255 + THRESHOLD) && r_255 > (b_255 + THRESHOLD)) {
            return COLOR_RED;
        } else {
            return COLOR_UNKNOWN;  // Not clearly red
        }
    } else if (g_255 > r_255 && g_255 > b_255) {
        // Green is dominant
        if (g_255 > (r_255 + THRESHOLD) && g_255 > (b_255 + THRESHOLD)) {
            return COLOR_GREEN;
        } else {
            return COLOR_UNKNOWN;  // Not clearly green
        }
    } else if (b_255 > r_255 && b_255 > g_255) {
        // Blue is dominant
        if (b_255 > (r_255 + THRESHOLD) && b_255 > (g_255 + THRESHOLD)) {
            return COLOR_BLUE;
        } else {
            return COLOR_UNKNOWN;  // Not clearly blue
        }
    } else {
        // No clear dominant color
        return COLOR_UNKNOWN;
    }
}

/**
 * Calculate RGB color from raw sensor values
 * 
 * @param r_raw: Raw RED sensor value (0-65535)
 * @param g_raw: Raw GREEN sensor value (0-65535)
 * @param b_raw: Raw BLUE sensor value (0-65535)
 * @param w_raw: Raw WHITE sensor value (0-65535)
 * @param rgb: Output structure to be filled
 * @return: Final color classification
 */
RGB_color_type_t calculate_RGB_color_v2(uint16_t r_raw, uint16_t g_raw, uint16_t b_raw, uint16_t w_raw, 
                                        struct RGB_color_data_t *rgb) {
    // Step 1: Predict RGB values using trained model (0-255 scale)
    float r_255 = predict_channel(r_raw, g_raw, b_raw, w_raw, &MODEL_R);
    float g_255 = predict_channel(r_raw, g_raw, b_raw, w_raw, &MODEL_G);
    float b_255 = predict_channel(r_raw, g_raw, b_raw, w_raw, &MODEL_B);
    
    // Step 2: Convert RGB to 0-100 scale
    rgb->red = scale_255_to_100(r_255);
    rgb->green = scale_255_to_100(g_255);
    rgb->blue = scale_255_to_100(b_255);
    
    // Step 3: Calculate White and Black components (0-100 scale)
    calculate_white_black(r_255, g_255, b_255, &rgb->white, &rgb->black);
    
    // Step 4: Classify color
    rgb->color = classify_color(r_255, g_255, b_255);
    
    // Brightness is not implemented (as requested)
    rgb->brightness = 0;
    
    return rgb->color;
}

// Example usage
#ifdef EXAMPLE_USAGE
#include <stdio.h>

int main(void) {
    struct RGB_color_data_t rgb;
    RGB_color_type_t result;
    
    // Example 1: Red object
    printf("Example 1: Red object\n");
    result = calculate_RGB_color_v2(1325, 921, 364, 2096, &rgb);
    printf("  R=%u, G=%u, B=%u, W=%u, K=%u\n", 
           rgb.red, rgb.green, rgb.blue, rgb.white, rgb.black);
    printf("  Color: %s\n", 
           result == COLOR_RED ? "RED" :
           result == COLOR_GREEN ? "GREEN" :
           result == COLOR_BLUE ? "BLUE" :
           result == COLOR_WHITE ? "WHITE" :
           result == COLOR_BLACK ? "BLACK" : "UNKNOWN");
    printf("\n");
    
    // Example 2: White object
    printf("Example 2: White object\n");
    result = calculate_RGB_color_v2(2400, 2400, 2400, 4000, &rgb);
    printf("  R=%u, G=%u, B=%u, W=%u, K=%u\n", 
           rgb.red, rgb.green, rgb.blue, rgb.white, rgb.black);
    printf("  Color: %s\n", 
           result == COLOR_RED ? "RED" :
           result == COLOR_GREEN ? "GREEN" :
           result == COLOR_BLUE ? "BLUE" :
           result == COLOR_WHITE ? "WHITE" :
           result == COLOR_BLACK ? "BLACK" : "UNKNOWN");
    printf("\n");
    
    // Example 3: Black object
    printf("Example 3: Black object\n");
    result = calculate_RGB_color_v2(200, 200, 200, 400, &rgb);
    printf("  R=%u, G=%u, B=%u, W=%u, K=%u\n", 
           rgb.red, rgb.green, rgb.blue, rgb.white, rgb.black);
    printf("  Color: %s\n", 
           result == COLOR_RED ? "RED" :
           result == COLOR_GREEN ? "GREEN" :
           result == COLOR_BLUE ? "BLUE" :
           result == COLOR_WHITE ? "WHITE" :
           result == COLOR_BLACK ? "BLACK" : "UNKNOWN");
    
    return 0;
}
#endif

