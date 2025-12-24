/**
 * @file rgb_color_sensor.h
 * @brief RGB Color Sensor Calibration and Classification
 * 
 * This header file provides functions for RGB color sensor data processing,
 * including machine learning-based calibration and color classification.
 * 
 * Based on Python model training from train_rgb_model.py
 */

#ifndef RGB_COLOR_SENSOR_H
#define RGB_COLOR_SENSOR_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * RGB color classification types
 */
typedef enum RGB_color_type_t {
    COLOR_UNKNOWN = 0,  ///< Unknown or unclear color
    COLOR_RED,          ///< Red dominant
    COLOR_GREEN,        ///< Green dominant
    COLOR_BLUE,         ///< Blue dominant
    COLOR_WHITE,        ///< White (high brightness, low saturation)
    COLOR_BLACK,        ///< Black (very dark)
} RGB_color_type_t;

/**
 * RGB color sensor data structure
 */
struct RGB_color_data_t {
    uint16_t r_raw;         ///< RAW RED sensor value (0-65535)
    uint16_t g_raw;         ///< RAW GREEN sensor value (0-65535)
    uint16_t b_raw;         ///< RAW BLUE sensor value (0-65535)
    uint16_t w_raw;         ///< RAW WHITE sensor value (0-65535)
    uint8_t red;            ///< Calibrated RED value (0-100 scale)
    uint8_t green;          ///< Calibrated GREEN value (0-100 scale)
    uint8_t blue;           ///< Calibrated BLUE value (0-100 scale)
    uint8_t white;          ///< WHITE component (0-100 scale)
    uint8_t black;          ///< BLACK component (0-100 scale)
    uint8_t color;          ///< Final color classification (RGB_color_type_t)
    uint8_t brightness;     ///< Reserved (not implemented)
};

/**
 * @brief Calculate RGB color from raw sensor values
 * 
 * This function processes raw RGBW sensor values through a trained machine learning
 * model to produce calibrated RGB values, calculate White/Black components using
 * Color Theory, and classify the final color.
 * 
 * Processing steps:
 * 1. Apply linear regression model to predict RGB (0-255 scale)
 * 2. Convert RGB to 0-100 scale
 * 3. Calculate White = min(R,G,B) and Black = 255-max(R,G,B)
 * 4. Convert White/Black to 0-100 scale
 * 5. Classify color based on RGB dominance
 * 
 * @param r_raw Raw RED sensor value (0-65535, 16-bit)
 * @param g_raw Raw GREEN sensor value (0-65535, 16-bit)
 * @param b_raw Raw BLUE sensor value (0-65535, 16-bit)
 * @param w_raw Raw WHITE sensor value (0-65535, 16-bit)
 * @param rgb Pointer to RGB_color_data_t structure to be filled with results
 * 
 * @return RGB_color_type_t Final color classification
 * 
 * @note Model coefficients should be updated with actual trained values
 *       from rgb_model_coefficients.h
 * 
 * @example
 * struct RGB_color_data_t rgb;
 * RGB_color_type_t color = calculate_RGB_color_v2(1325, 921, 364, 2096, &rgb);
 * printf("Color: %s, R=%u, G=%u, B=%u\n", 
 *        color == COLOR_RED ? "RED" : "OTHER",
 *        rgb.red, rgb.green, rgb.blue);
 */
RGB_color_type_t calculate_RGB_color_v2(uint16_t r_raw, uint16_t g_raw, uint16_t b_raw, uint16_t w_raw, 
                                        struct RGB_color_data_t *rgb);

/**
 * @brief Get color name as string
 * 
 * @param color Color type enum value
 * @return const char* Color name string
 */
static inline const char* rgb_color_to_string(RGB_color_type_t color) {
    switch (color) {
        case COLOR_RED:     return "Red";
        case COLOR_GREEN:   return "Green";
        case COLOR_BLUE:    return "Blue";
        case COLOR_WHITE:   return "White";
        case COLOR_BLACK:   return "Black";
        case COLOR_UNKNOWN:
        default:            return "Unknown";
    }
}

#ifdef __cplusplus
}
#endif

#endif /* RGB_COLOR_SENSOR_H */

