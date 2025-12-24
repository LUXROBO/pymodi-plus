/* Auto-generated RGB sensor calibration coefficients */
/* Generated from train_rgb_model.py */

#ifndef RGB_MODEL_COEFFICIENTS_H
#define RGB_MODEL_COEFFICIENTS_H

/* R channel coefficients */
const float weights_r[4] = {
    -0.0046080002f,  /* RAW_R coefficient */
    -0.1451801105f,  /* RAW_G coefficient */
    -0.1066228002f,  /* RAW_B coefficient */
    0.1828643255f   /* RAW_W coefficient */
};
const float bias_r = 27.8251291260f;

/* G channel coefficients */
const float weights_g[4] = {
    0.0580512560f,  /* RAW_R coefficient */
    0.1986500163f,  /* RAW_G coefficient */
    0.0037366550f,  /* RAW_B coefficient */
    -0.1107949361f   /* RAW_W coefficient */
};
const float bias_g = 66.9992062401f;

/* B channel coefficients */
const float weights_b[4] = {
    -0.0379945661f,  /* RAW_R coefficient */
    -0.0701221433f,  /* RAW_G coefficient */
    0.2547709696f,  /* RAW_B coefficient */
    0.0148413837f   /* RAW_W coefficient */
};
const float bias_b = 49.9436550292f;

/* Prediction functions */
static inline float predict_r(float raw_r, float raw_g, float raw_b, float raw_w) {
    float result = weights_r[0] * raw_r + 
                   weights_r[1] * raw_g + 
                   weights_r[2] * raw_b + 
                   weights_r[3] * raw_w + 
                   bias_r;
    
    /* Clip to valid range [0, 255] */
    if (result < 0.0f) result = 0.0f;
    if (result > 255.0f) result = 255.0f;
    
    return result;
}

static inline float predict_g(float raw_r, float raw_g, float raw_b, float raw_w) {
    float result = weights_g[0] * raw_r + 
                   weights_g[1] * raw_g + 
                   weights_g[2] * raw_b + 
                   weights_g[3] * raw_w + 
                   bias_g;
    
    /* Clip to valid range [0, 255] */
    if (result < 0.0f) result = 0.0f;
    if (result > 255.0f) result = 255.0f;
    
    return result;
}

static inline float predict_b(float raw_r, float raw_g, float raw_b, float raw_w) {
    float result = weights_b[0] * raw_r + 
                   weights_b[1] * raw_g + 
                   weights_b[2] * raw_b + 
                   weights_b[3] * raw_w + 
                   bias_b;
    
    /* Clip to valid range [0, 255] */
    if (result < 0.0f) result = 0.0f;
    if (result > 255.0f) result = 255.0f;
    
    return result;
}

#endif /* RGB_MODEL_COEFFICIENTS_H */
