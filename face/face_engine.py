
import math
import pygame

from face.colors import BG
from face.eyes import draw_eye
from face.eyebrows import draw_eyebrow
from face.mouth import draw_mouth

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
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.emotion = "neutral"
        self.intensity = 1.0
        self.time = 0.0

        self.blink = BlinkAnimation()
        self.breathing = BreathingAnimation()

        neutral = EMOTION_PRESETS["neutral"]

        self.eye_open = SmoothValue(neutral["eye_open"])
        self.eyebrow_height = SmoothValue(
            neutral["eyebrow_height"]
        )
        self.eyebrow_angle = SmoothValue(
            neutral["eyebrow_angle"]
        )
        self.smile = SmoothValue(neutral["smile"])
        self.mouth_open = SmoothValue(
            neutral["mouth_open"]
        )

        self.breathe = 0.0

        # Suivi par webcam
        self.vision_enabled = True
        self.face_detected = False

        self.vision_x = 0.0
        self.vision_y = 0.0

        # Position affichee du regard
        self.look_x = 0.0
        self.look_y = 0.0

        # Vitesse de transition du regard
        self.look_speed = 7.0

    def set_emotion(self, emotion, intensity=1.0):
        if emotion not in VALID_EMOTIONS:
            print("Emotion inconnue :", emotion)
            return

        self.emotion = emotion
        self.intensity = clamp(intensity, 0.0, 1.0)

        neutral = EMOTION_PRESETS["neutral"]
        target = EMOTION_PRESETS[emotion]

        def mix(parameter):
            return (
                neutral[parameter]
                + (
                    target[parameter] - neutral[parameter]
                ) * self.intensity
            )

        self.eye_open.set_target(mix("eye_open"))
        self.eyebrow_height.set_target(
            mix("eyebrow_height")
        )
        self.eyebrow_angle.set_target(
            mix("eyebrow_angle")
        )
        self.smile.set_target(mix("smile"))
        self.mouth_open.set_target(
            mix("mouth_open")
        )

    def set_vision_position(
        self,
        detected,
        x=0.0,
        y=0.0
    ):
        self.face_detected = bool(detected)

        if detected:
            self.vision_x = clamp(
                float(x), -1.0, 1.0
            )
            self.vision_y = clamp(
                float(y), -1.0, 1.0
            )

    def set_vision_enabled(self, enabled):
        self.vision_enabled = bool(enabled)

        if not enabled:
            self.face_detected = False

    def _get_target_look(self):
        if (
            self.vision_enabled
            and self.face_detected
        ):
            return self.vision_x, self.vision_y

        mx, my = pygame.mouse.get_pos()

        look_x = clamp(
            (mx - self.width / 2)
            / (self.width / 2),
            -1.0,
            1.0
        )

        look_y = clamp(
            (my - self.height / 2)
            / (self.height / 2),
            -1.0,
            1.0
        )

        if self.emotion == "thinking":
            look_x = 0.45
            look_y = -0.55

        return look_x, look_y

    def update(self, dt):
        self.time += dt

        self.blink.update(dt)
        self.breathe = self.breathing.update(dt)

        for value in (
            self.eye_open,
            self.eyebrow_height,
            self.eyebrow_angle,
            self.smile,
            self.mouth_open
        ):
            value.update(dt)

        target_x, target_y = self._get_target_look()

        # Lissage independant du FPS
        factor = 1.0 - math.exp(
            -self.look_speed * max(0.0, dt)
        )

        self.look_x += (
            target_x - self.look_x
        ) * factor

        self.look_y += (
            target_y - self.look_y
        ) * factor

    def get_look_direction(self):
        return self.look_x, self.look_y

    def draw(self, surface):
        surface.fill(BG)

        look_x, look_y = self.get_look_direction()

        left_x = 340
        right_x = 560

        eye_y = 290 + self.breathe
        eyebrow_y = 185 + self.breathe

        for side, x in (
            ("left", left_x),
            ("right", right_x)
        ):
            draw_eyebrow(
                surface,
                x,
                eyebrow_y,
                side,
                self.eyebrow_height.current,
                self.eyebrow_angle.current
            )

            draw_eye(
                surface,
                x,
                eye_y,
                side,
                self.blink.value,
                self.eye_open.current,
                look_x,
                look_y
            )

        talking_amount = 0.0

        if self.emotion == "talking":
            talking_amount = (
                0.25
                + abs(math.sin(self.time * 9)) * 0.75
            )

        draw_mouth(
            surface,
            self.width // 2,
            425,
            self.smile.current,
            self.mouth_open.current,
            talking_amount
        )
