import pygame

from face.colors import (
    CYAN,
    CYAN_BRIGHT,
    CYAN_SOFT,
    WHITE,
    WHITE_BLUE,
    PUPIL
)


# ============================================================
# GLOW
# ============================================================

def glow_ellipse(
    surface,
    rect,
    color,
    strength=4
):

    glow = pygame.Surface(
        surface.get_size(),
        pygame.SRCALPHA
    )

    for i in range(
        strength,
        0,
        -1
    ):

        expanded = rect.inflate(
            i * 8,
            i * 8
        )

        alpha = int(
            12 / i
        )

        pygame.draw.ellipse(
            glow,
            (
                color[0],
                color[1],
                color[2],
                alpha
            ),
            expanded,
            4
        )

    surface.blit(
        glow,
        (0, 0)
    )


# ============================================================
# OEIL
# ============================================================

def draw_eye(
    surface,
    cx,
    cy,
    side,
    blink_value,
    eye_open,
    look_x,
    look_y
):

    # --------------------------------------------------------
    # Dimensions
    # --------------------------------------------------------

    eye_w = 175

    base_height = 145

    eye_h = (
        base_height
        * eye_open
    )

    current_h = max(
        8,
        int(
            eye_h
            * blink_value
        )
    )

    # --------------------------------------------------------
    # Contour
    # --------------------------------------------------------

    outer_rect = pygame.Rect(
        int(cx - eye_w / 2),
        int(cy - current_h / 2),
        eye_w,
        current_h
    )

    glow_ellipse(
        surface,
        outer_rect,
        CYAN,
        5
    )

    pygame.draw.ellipse(
        surface,
        CYAN_SOFT,
        outer_rect,
        10
    )

    pygame.draw.ellipse(
        surface,
        CYAN,
        outer_rect.inflate(
            -10,
            -8
        ),
        5
    )

    # --------------------------------------------------------
    # Oeil fermé
    # --------------------------------------------------------

    if blink_value < 0.15:

        pygame.draw.line(
            surface,
            CYAN,
            (
                cx - eye_w // 2 + 20,
                cy
            ),
            (
                cx + eye_w // 2 - 20,
                cy
            ),
            6
        )

        return

    # --------------------------------------------------------
    # Blanc
    # --------------------------------------------------------

    white_rect = pygame.Rect(
        int(cx - eye_w / 2 + 24),
        int(cy - current_h / 2 + 20),
        eye_w - 48,
        max(
            5,
            current_h - 40
        )
    )

    pygame.draw.ellipse(
        surface,
        WHITE_BLUE,
        white_rect
    )

    # --------------------------------------------------------
    # Position pupille
    # --------------------------------------------------------

    max_x = 25
    max_y = 16

    pupil_x = (
        cx
        + look_x * max_x
    )

    pupil_y = (
        cy
        + look_y * max_y
    )

    # Asymétrie légère
    if side == "left":
        pupil_x += 2

    else:
        pupil_x -= 2

    # --------------------------------------------------------
    # Iris
    # --------------------------------------------------------

    iris_w = 58
    iris_h = 75

    iris_rect = pygame.Rect(
        int(pupil_x - iris_w / 2),
        int(pupil_y - iris_h / 2),
        iris_w,
        iris_h
    )

    iris_glow = pygame.Surface(
        surface.get_size(),
        pygame.SRCALPHA
    )

    pygame.draw.ellipse(
        iris_glow,
        (
            30,
            220,
            255,
            45
        ),
        iris_rect.inflate(
            14,
            14
        )
    )

    surface.blit(
        iris_glow,
        (0, 0)
    )

    pygame.draw.ellipse(
        surface,
        CYAN,
        iris_rect
    )

    # --------------------------------------------------------
    # Pupille
    # --------------------------------------------------------

    pupil_rect = pygame.Rect(
        int(pupil_x - 20),
        int(pupil_y - 29),
        40,
        58
    )

    pygame.draw.ellipse(
        surface,
        PUPIL,
        pupil_rect
    )

    # --------------------------------------------------------
    # Reflet principal
    # --------------------------------------------------------

    pygame.draw.ellipse(
        surface,
        WHITE,
        (
            int(pupil_x - 15),
            int(pupil_y - 23),
            15,
            19
        )
    )

    # --------------------------------------------------------
    # Reflet cyan
    # --------------------------------------------------------

    pygame.draw.circle(
        surface,
        CYAN_BRIGHT,
        (
            int(pupil_x + 10),
            int(pupil_y + 14)
        ),
        5
    )

    # --------------------------------------------------------
    # Petit reflet blanc
    # --------------------------------------------------------

    pygame.draw.circle(
        surface,
        WHITE,
        (
            int(pupil_x + 13),
            int(pupil_y - 8)
        ),
        3
    )