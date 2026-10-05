# ============================================================
# EMOTIONS
# ============================================================

NEUTRAL = "neutral"
HAPPY = "happy"
SAD = "sad"
ANGRY = "angry"
SURPRISED = "surprised"
THINKING = "thinking"
LISTENING = "listening"
TALKING = "talking"


VALID_EMOTIONS = {
    NEUTRAL,
    HAPPY,
    SAD,
    ANGRY,
    SURPRISED,
    THINKING,
    LISTENING,
    TALKING,
}


# ============================================================
# PARAMETRES DES EXPRESSIONS
# ============================================================

EMOTION_PRESETS = {

    NEUTRAL: {
        "eye_open": 1.00,
        "eyebrow_height": 0.00,
        "eyebrow_angle": 0.00,
        "smile": 0.00,
        "mouth_open": 0.00,
    },

    HAPPY: {
        "eye_open": 0.85,
        "eyebrow_height": 0.15,
        "eyebrow_angle": 0.00,
        "smile": 1.00,
        "mouth_open": 0.10,
    },

    SAD: {
        "eye_open": 0.85,
        "eyebrow_height": 0.05,
        "eyebrow_angle": 0.65,
        "smile": -0.80,
        "mouth_open": 0.00,
    },

    ANGRY: {
        "eye_open": 0.75,
        "eyebrow_height": -0.10,
        "eyebrow_angle": -0.90,
        "smile": -0.25,
        "mouth_open": 0.00,
    },

    SURPRISED: {
        "eye_open": 1.15,
        "eyebrow_height": 0.45,
        "eyebrow_angle": 0.00,
        "smile": 0.00,
        "mouth_open": 1.00,
    },

    THINKING: {
        "eye_open": 0.90,
        "eyebrow_height": 0.15,
        "eyebrow_angle": 0.20,
        "smile": 0.05,
        "mouth_open": 0.00,
    },

    LISTENING: {
        "eye_open": 1.05,
        "eyebrow_height": 0.15,
        "eyebrow_angle": 0.00,
        "smile": 0.08,
        "mouth_open": 0.00,
    },

    TALKING: {
        "eye_open": 1.00,
        "eyebrow_height": 0.05,
        "eyebrow_angle": 0.00,
        "smile": 0.20,
        "mouth_open": 0.50,
    },
}