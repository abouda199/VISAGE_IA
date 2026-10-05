from face.emotions import EMOTION_PRESETS, VALID_EMOTIONS


def lerp(a, b, t):
    """
    Interpolation linéaire.
    """
    return a + (b - a) * t


class EmotionEngine:

    def __init__(self):

        self.emotion = "neutral"
        self.intensity = 1.0

        # Paramètres actuels
        self.current = EMOTION_PRESETS["neutral"].copy()

        # Paramètres désirés
        self.target = EMOTION_PRESETS["neutral"].copy()

        # Vitesse de transition
        self.transition_speed = 5.0

    # ========================================================
    # CHANGER EMOTION
    # ========================================================

    def set_emotion(
        self,
        emotion,
        intensity=1.0
    ):

        if emotion not in VALID_EMOTIONS:
            print(
                f"[EmotionEngine] Emotion inconnue : {emotion}"
            )
            return

        intensity = max(
            0.0,
            min(1.0, intensity)
        )

        self.emotion = emotion
        self.intensity = intensity

        neutral = EMOTION_PRESETS["neutral"]
        preset = EMOTION_PRESETS[emotion]

        # Mélange neutral -> emotion
        self.target = {}

        for parameter in preset:

            neutral_value = neutral[parameter]
            emotion_value = preset[parameter]

            self.target[parameter] = (
                neutral_value
                + (
                    emotion_value
                    - neutral_value
                )
                * intensity
            )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt):

        factor = min(
            1.0,
            dt * self.transition_speed
        )

        for parameter in self.current:

            self.current[parameter] = lerp(
                self.current[parameter],
                self.target[parameter],
                factor
            )

    # ========================================================
    # GET
    # ========================================================

    def get(self, parameter):

        return self.current.get(
            parameter,
            0.0
        )