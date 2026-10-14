
# ============================================================
# VISAGE-AI - EMOTIONS
# ============================================================

NEUTRAL = "neutral"
HAPPY = "happy"
SAD = "sad"
ANGRY = "angry"
SURPRISED = "surprised"
THINKING = "thinking"
LISTENING = "listening"
TALKING = "talking"

# Nouvelles expressions
WINK = "wink"
EXCITED = "excited"
LOVE = "love"
SLEEPY = "sleepy"
CONFUSED = "confused"

EMOTION_PRESETS = {
    NEUTRAL: {
        "eye_open": 1.0,
        "eyebrow_height": 0.0,
        "eyebrow_angle": 0.0,
        "smile": 0.0,
        "mouth_open": 0.0,
    },
    HAPPY: {
        "eye_open": 0.85,
        "eyebrow_height": 0.15,
        "eyebrow_angle": 0.0,
        "smile": 1.0,
        "mouth_open": 0.1,
    },
    SAD: {
        "eye_open": 0.85,
        "eyebrow_height": 0.05,
        "eyebrow_angle": 0.65,
        "smile": -0.8,
        "mouth_open": 0.0,
    },
    ANGRY: {
        "eye_open": 0.75,
        "eyebrow_height": -0.1,
        "eyebrow_angle": -0.9,
        "smile": -0.25,
        "mouth_open": 0.0,
    },
    SURPRISED: {
        "eye_open": 1.15,
        "eyebrow_height": 0.45,
        "eyebrow_angle": 0.0,
        "smile": 0.0,
        "mouth_open": 1.0,
    },
    THINKING: {
        "eye_open": 0.9,
        "eyebrow_height": 0.15,
        "eyebrow_angle": 0.2,
        "smile": 0.05,
        "mouth_open": 0.0,
    },
    LISTENING: {
        "eye_open": 1.05,
        "eyebrow_height": 0.15,
        "eyebrow_angle": 0.0,
        "smile": 0.08,
        "mouth_open": 0.0,
    },
    TALKING: {
        "eye_open": 1.0,
        "eyebrow_height": 0.05,
        "eyebrow_angle": 0.0,
        "smile": 0.2,
        "mouth_open": 0.5,
    },
    WINK: {
        "eye_open": 1.0,
        "eyebrow_height": 0.15,
        "eyebrow_angle": 0.0,
        "smile": 0.95,
        "mouth_open": 0.0,
    },
    EXCITED: {
        "eye_open": 0.7,
        "eyebrow_height": 0.25,
        "eyebrow_angle": 0.0,
        "smile": 1.0,
        "mouth_open": 0.15,
    },
    LOVE: {
        "eye_open": 0.95,
        "eyebrow_height": 0.2,
        "eyebrow_angle": 0.0,
        "smile": 0.85,
        "mouth_open": 0.05,
    },
    SLEEPY: {
        "eye_open": 0.35,
        "eyebrow_height": -0.1,
        "eyebrow_angle": 0.0,
        "smile": 0.0,
        "mouth_open": 0.0,
    },
    CONFUSED: {
        "eye_open": 0.9,
        "eyebrow_height": 0.15,
        "eyebrow_angle": 0.3,
        "smile": -0.1,
        "mouth_open": 0.05,
    },
}

VALID_EMOTIONS = set(EMOTION_PRESETS.keys())
