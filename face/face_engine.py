import pygame
import math

from face.colors import BG

from face.eyes import draw_eye

from face.eyebrows import (
    draw_eyebrow
)

from face.mouth import (
    draw_mouth
)

from face.animations import (
    BlinkAnimation,
    BreathingAnimation,
    SmoothValue,
    clamp
)

from face.emotions import (
    EMOTION_PRESETS,
    VALID_EMOTIONS
)


class FaceEngine:

    def __init__(
        self,
        width,
        height
    ):

        self.width = width
        self.height = height

        # ====================================================
        # ETAT
        # ====================================================

        self.emotion = "neutral"

        self.intensity = 1.0

        self.time = 0.0

        # ====================================================
        # ANIMATIONS
        # ====================================================

        self.blink = BlinkAnimation()

        self.breathing = (
            BreathingAnimation()
        )

        # ====================================================
        # PARAMETRES FLUIDES
        # ====================================================

        neutral = (
            EMOTION_PRESETS["neutral"]
        )

        self.eye_open = SmoothValue(
            neutral["eye_open"]
        )

        self.eyebrow_height = SmoothValue(
            neutral["eyebrow_height"]
        )

        self.eyebrow_angle = SmoothValue(
            neutral["eyebrow_angle"]
        )

        self.smile = SmoothValue(
            neutral["smile"]
        )

        self.mouth_open = SmoothValue(
            neutral["mouth_open"]
        )

        self.breathe = 0.0

    # ========================================================
    # SET EMOTION
    # ========================================================

    def set_emotion(
        self,
        emotion,
        intensity=1.0
    ):

        if emotion not in VALID_EMOTIONS:

            print(
                "Emotion inconnue :",
                emotion
            )

            return

        self.emotion = emotion

        self.intensity = clamp(
            intensity,
            0.0,
            1.0
        )

        neutral = (
            EMOTION_PRESETS["neutral"]
        )

        target = (
            EMOTION_PRESETS[emotion]
        )

        def mix(parameter):

            return (
                neutral[parameter]
                +
                (
                    target[parameter]
                    - neutral[parameter]
                )
                * self.intensity
            )

        self.eye_open.set_target(
            mix("eye_open")
        )

        self.eyebrow_height.set_target(
            mix("eyebrow_height")
        )

        self.eyebrow_angle.set_target(
            mix("eyebrow_angle")
        )

        self.smile.set_target(
            mix("smile")
        )

        self.mouth_open.set_target(
            mix("mouth_open")
        )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt):

        self.time += dt

        self.blink.update(dt)

        self.breathe = (
            self.breathing.update(dt)
        )

        self.eye_open.update(dt)

        self.eyebrow_height.update(dt)

        self.eyebrow_angle.update(dt)

        self.smile.update(dt)

        self.mouth_open.update(dt)

    # ========================================================
    # REGARD SOURIS
    # ========================================================

    def get_look_direction(self):

        mx, my = pygame.mouse.get_pos()

        center_x = (
            self.width / 2
        )

        center_y = (
            self.height / 2
        )

        dx = (
            mx - center_x
        )

        dy = (
            my - center_y
        )

        look_x = clamp(
            dx / center_x,
            -1.0,
            1.0
        )

        look_y = clamp(
            dy / center_y,
            -1.0,
            1.0
        )

        # Thinking :
        # regard automatique vers le haut
        if self.emotion == "thinking":

            look_x = 0.45
            look_y = -0.55

        return (
            look_x,
            look_y
        )

    # ========================================================
    # DESSIN
    # ========================================================

    def draw(self, surface):

        surface.fill(BG)

        look_x, look_y = (
            self.get_look_direction()
        )

        # ====================================================
        # POSITIONS
        # ====================================================

        left_x = 340
        right_x = 560

        eye_y = (
            290
            + self.breathe
        )

        eyebrow_y = (
            185
            + self.breathe
        )

        # ====================================================
        # SOURCILS
        # ====================================================

        draw_eyebrow(
            surface,
            left_x,
            eyebrow_y,
            "left",
            self.eyebrow_height.current,
            self.eyebrow_angle.current
        )

        draw_eyebrow(
            surface,
            right_x,
            eyebrow_y,
            "right",
            self.eyebrow_height.current,
            self.eyebrow_angle.current
        )

        # ====================================================
        # YEUX
        # ====================================================

        draw_eye(
            surface,
            left_x,
            eye_y,
            "left",
            self.blink.value,
            self.eye_open.current,
            look_x,
            look_y
        )

        draw_eye(
            surface,
            right_x,
            eye_y,
            "right",
            self.blink.value,
            self.eye_open.current,
            look_x,
            look_y
        )

        # ====================================================
        # TALKING
        # ====================================================

        talking_amount = 0.0

        if self.emotion == "talking":

            talking_amount = (
                0.25
                +
                abs(
                    math.sin(
                        self.time * 9
                    )
                )
                * 0.75
            )

        # ====================================================
        # BOUCHE
        # ====================================================

        draw_mouth(
            surface,
            self.width // 2,
            425,
            self.smile.current,
            self.mouth_open.current,
            talking_amount
        )