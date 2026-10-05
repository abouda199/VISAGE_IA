import pygame
import math

from face.colors import (
    CYAN
)


def draw_eyebrow(
    surface,
    center_x,
    center_y,
    side,
    height_value,
    angle_value
):

    width = 120
    height = 45

    # ========================================================
    # HAUTEUR
    # ========================================================

    offset_y = (
        -height_value
        * 45
    )

    # ========================================================
    # ANGLE
    # ========================================================

    rotation = 0

    if side == "left":

        rotation = (
            angle_value
            * 18
        )

    else:

        rotation = (
            -angle_value
            * 18
        )

    # ========================================================
    # SURFACE SOURCIL
    # ========================================================

    eyebrow_surface = pygame.Surface(
        (160, 90),
        pygame.SRCALPHA
    )

    rect = pygame.Rect(
        20,
        25,
        width,
        height
    )

    # Glow
    pygame.draw.arc(
        eyebrow_surface,
        (
            30,
            170,
            210,
            80
        ),
        rect.inflate(
            8,
            8
        ),
        math.radians(195),
        math.radians(345),
        10
    )

    # Sourcil principal
    pygame.draw.arc(
        eyebrow_surface,
        CYAN,
        rect,
        math.radians(195),
        math.radians(345),
        7
    )

    # Rotation
    eyebrow_surface = (
        pygame.transform.rotate(
            eyebrow_surface,
            rotation
        )
    )

    surface.blit(
        eyebrow_surface,
        (
            center_x
            - eyebrow_surface.get_width() // 2,

            center_y
            + offset_y
            - eyebrow_surface.get_height() // 2
        )
    )