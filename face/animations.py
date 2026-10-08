
import random
import math


# ============================================================
# OUTILS MATHEMATIQUES
# ============================================================

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def lerp(a, b, amount):
    return a + (b - a) * amount


def smoothstep(value):
    value = clamp(value, 0.0, 1.0)
    return value * value * (3.0 - 2.0 * value)


# ============================================================
# CLIGNEMENT NATUREL DES YEUX
# ============================================================

class BlinkAnimation:

    def __init__(self):

        self.value = 1.0

        self.blinking = False

        self.time = 0.0
        self.blink_start = 0.0

        self.duration = 0.16

        self.next_blink = random.uniform(
            2.0, 4.5
        )

        self.double_blink = False

    def update(self, dt):

        dt = max(0.0, dt)
        self.time += dt

        # --------------------------------------------
        # ATTENTE AVANT LE PROCHAIN CLIGNEMENT
        # --------------------------------------------

        if not self.blinking:

            if self.time >= self.next_blink:

                self.blinking = True
                self.blink_start = self.time

                self.duration = random.uniform(
                    0.13, 0.20
                )

        # --------------------------------------------
        # ANIMATION DU CLIGNEMENT
        # --------------------------------------------

        if self.blinking:

            progress = (
                self.time - self.blink_start
            ) / self.duration

            if progress < 0.40:

                # Fermeture rapide
                p = smoothstep(
                    progress / 0.40
                )

                self.value = lerp(
                    1.0, 0.04, p
                )

            elif progress < 1.0:

                # Ouverture plus lente
                p = smoothstep(
                    (progress - 0.40) / 0.60
                )

                self.value = lerp(
                    0.04, 1.0, p
                )

            else:

                self.value = 1.0
                self.blinking = False

                # Quelques doubles clignements
                if (
                    not self.double_blink
                    and random.random() < 0.12
                ):

                    self.double_blink = True

                    self.next_blink = (
                        self.time + 0.18
                    )

                else:

                    self.double_blink = False

                    self.next_blink = (
                        self.time
                        + random.uniform(
                            2.2, 5.0
                        )
                    )

        return self.value


# ============================================================
# RESPIRATION NATURELLE
# ============================================================

class BreathingAnimation:

    def __init__(self):

        self.time = 0.0

        self.speed = 1.15

        self.amplitude = 2.0

    def update(self, dt):

        self.time += max(0.0, dt)

        # Mouvement principal lent
        primary = math.sin(
            self.time * self.speed
        )

        # Très légère variation secondaire
        secondary = (
            math.sin(
                self.time * 0.47
            ) * 0.25
        )

        return (
            primary + secondary
        ) * self.amplitude


# ============================================================
# TRANSITIONS EMOTIONNELLES FLUIDES
# ============================================================

class SmoothValue:

    def __init__(
        self,
        value=0.0,
        speed=5.0
    ):

        self.current = float(value)
        self.target = float(value)

        self.speed = float(speed)

    def set_target(self, value):

        self.target = float(value)

    def update(self, dt):

        dt = max(0.0, dt)

        # Interpolation exponentielle :
        # comportement stable même si le FPS varie
        factor = (
            1.0 - math.exp(
                -self.speed * dt
            )
        )

        self.current = lerp(
            self.current,
            self.target,
            factor
        )

        # Évite les petites oscillations numériques
        if abs(
            self.current - self.target
        ) < 0.0001:

            self.current = self.target

        return self.current


# ============================================================
# MICRO-MOUVEMENTS NATURELS
# ============================================================

class MicroMovement:

    def __init__(
        self,
        amplitude=1.0,
        speed=1.0
    ):

        self.time = 0.0

        self.amplitude = amplitude
        self.speed = speed

        self.phase = random.uniform(
            0.0,
            2.0 * math.pi
        )

    def update(self, dt):

        self.time += max(0.0, dt)

        movement_1 = math.sin(
            self.time * self.speed
            + self.phase
        )

        movement_2 = (
            math.sin(
                self.time * self.speed * 0.37
                + self.phase * 0.7
            )
            * 0.35
        )

        return (
            movement_1 + movement_2
        ) * self.amplitude
