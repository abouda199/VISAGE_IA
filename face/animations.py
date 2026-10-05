import pygame
import random
import math


# ============================================================
# OUTILS
# ============================================================

def clamp(value, minimum, maximum):
    return max(
        minimum,
        min(maximum, value)
    )


def lerp(a, b, amount):
    return a + (b - a) * amount


# ============================================================
# CLIGNEMENT
# ============================================================

class BlinkAnimation:

    def __init__(self):

        self.value = 1.0

        self.blinking = False

        self.direction = -1

        self.next_blink = (
            pygame.time.get_ticks()
            + random.randint(2500, 5000)
        )

    def update(self, dt):

        now = pygame.time.get_ticks()

        # Commencer un clignement
        if (
            not self.blinking
            and now >= self.next_blink
        ):
            self.blinking = True
            self.direction = -1

        # Animation
        if self.blinking:

            self.value += (
                self.direction
                * dt
                * 9
            )

            # Fermeture complète
            if self.value <= 0.04:

                self.value = 0.04
                self.direction = 1

            # Réouverture
            elif self.value >= 1.0:

                self.value = 1.0

                self.blinking = False

                self.next_blink = (
                    now
                    + random.randint(
                        2500,
                        5500
                    )
                )

        return self.value


# ============================================================
# RESPIRATION / MOUVEMENT NATUREL
# ============================================================

class BreathingAnimation:

    def __init__(self):

        self.time = 0.0

    def update(self, dt):

        self.time += dt

        return (
            math.sin(
                self.time * 1.4
            )
            * 2
        )


# ============================================================
# TRANSITION EMOTIONNELLE
# ============================================================

class SmoothValue:

    def __init__(
        self,
        value=0.0,
        speed=5.0
    ):

        self.current = value
        self.target = value

        self.speed = speed

    def set_target(self, value):

        self.target = value

    def update(self, dt):

        factor = min(
            1.0,
            dt * self.speed
        )

        self.current = lerp(
            self.current,
            self.target,
            factor
        )

        return self.current