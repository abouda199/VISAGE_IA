import pygame
import math

from face.colors import (
    CYAN,
    CYAN_BRIGHT,
    CYAN_SOFT
)


# ============================================================
# OUTILS
# ============================================================

def quadratic_bezier(p0, p1, p2, steps=30):
    """
    Génère les points d'une courbe de Bézier quadratique.
    """
    points = []

    for i in range(steps + 1):

        t = i / steps

        x = (
            (1 - t) ** 2 * p0[0]
            + 2 * (1 - t) * t * p1[0]
            + t ** 2 * p2[0]
        )

        y = (
            (1 - t) ** 2 * p0[1]
            + 2 * (1 - t) * t * p1[1]
            + t ** 2 * p2[1]
        )

        points.append(
            (int(x), int(y))
        )

    return points


def draw_glow_line(
    surface,
    points,
    color,
    width=4
):
    """
    Léger halo derrière la bouche.
    """

    glow = pygame.Surface(
        surface.get_size(),
        pygame.SRCALPHA
    )

    if len(points) >= 2:

        pygame.draw.lines(
            glow,
            (
                color[0],
                color[1],
                color[2],
                40
            ),
            False,
            points,
            width + 7
        )

        pygame.draw.lines(
            surface,
            color,
            False,
            points,
            width
        )


# ============================================================
# BOUCHE NEUTRE
# ============================================================

def draw_neutral_mouth(
    surface,
    x,
    y
):

    # Petite bouche douce, pas une ligne parfaitement droite.

    points = quadratic_bezier(
        (x - 27, y),
        (x, y + 5),
        (x + 27, y)
    )

    draw_glow_line(
        surface,
        points,
        CYAN,
        4
    )


# ============================================================
# SOURIRE
# ============================================================

def draw_happy_mouth(
    surface,
    x,
    y,
    intensity
):

    intensity = max(
        0.0,
        min(1.0, intensity)
    )

    width = (
        32
        + 22 * intensity
    )

    depth = (
        8
        + 22 * intensity
    )

    # IMPORTANT :
    # En coordonnées écran, Y positif = vers le bas.
    #
    # Les extrémités sont donc PLUS HAUTES
    # que le centre pour créer un vrai sourire.

    left = (
        x - width,
        y - depth * 0.35
    )

    center = (
        x,
        y + depth
    )

    right = (
        x + width,
        y - depth * 0.35
    )

    points = quadratic_bezier(
        left,
        center,
        right
    )

    draw_glow_line(
        surface,
        points,
        CYAN_BRIGHT,
        5
    )

    # Petites commissures
    pygame.draw.circle(
        surface,
        CYAN_BRIGHT,
        (
            int(left[0]),
            int(left[1])
        ),
        3
    )

    pygame.draw.circle(
        surface,
        CYAN_BRIGHT,
        (
            int(right[0]),
            int(right[1])
        ),
        3
    )


# ============================================================
# BOUCHE TRISTE
# ============================================================

def draw_sad_mouth(
    surface,
    x,
    y,
    intensity
):

    intensity = max(
        0.0,
        min(1.0, intensity)
    )

    width = (
        32
        + 18 * intensity
    )

    depth = (
        8
        + 20 * intensity
    )

    # Centre PLUS HAUT.
    # Commissures PLUS BAS.
    #
    # => expression triste.

    left = (
        x - width,
        y + depth * 0.35
    )

    center = (
        x,
        y - depth
    )

    right = (
        x + width,
        y + depth * 0.35
    )

    points = quadratic_bezier(
        left,
        center,
        right
    )

    draw_glow_line(
        surface,
        points,
        CYAN,
        5
    )


# ============================================================
# BOUCHE OUVERTE PLUS NATURELLE
# ============================================================

def draw_open_mouth(
    surface,
    x,
    y,
    openness,
    smile=0.0
):

    openness = max(
        0.0,
        min(1.0, openness)
    )

    # Largeur supérieure à la hauteur :
    # évite l'effet "O / cercle".

    half_width = (
        25
        + 13 * openness
    )

    half_height = (
        5
        + 13 * openness
    )

    # Le sourire modifie légèrement les coins.
    corner_y = (
        y
        - max(0.0, smile) * 5
    )

    # -------------------------
    # Lèvre supérieure
    # -------------------------

    upper = quadratic_bezier(

        (
            x - half_width,
            corner_y
        ),

        (
            x,
            y - half_height
        ),

        (
            x + half_width,
            corner_y
        )
    )

    # -------------------------
    # Lèvre inférieure
    # -------------------------

    lower = quadratic_bezier(

        (
            x - half_width,
            corner_y
        ),

        (
            x,
            y + half_height
        ),

        (
            x + half_width,
            corner_y
        )
    )

    # -------------------------
    # Intérieur sombre
    # -------------------------

    polygon = (
        upper
        + list(reversed(lower))
    )

    pygame.draw.polygon(
        surface,
        (2, 12, 18),
        polygon
    )

    # -------------------------
    # Contours
    # -------------------------

    draw_glow_line(
        surface,
        upper,
        CYAN_BRIGHT,
        4
    )

    draw_glow_line(
        surface,
        lower,
        CYAN_BRIGHT,
        4
    )


# ============================================================
# BOUCHE PRINCIPALE
# ============================================================

def draw_mouth(
    surface,
    x,
    y,
    smile,
    mouth_open,
    talking_amount=0.0
):

    # ========================================================
    # 1. PAROLE
    # ========================================================

    if talking_amount > 0.05:

        # La bouche varie horizontalement ET verticalement.
        # Beaucoup plus naturel qu'une ellipse.

        openness = (
            0.15
            + talking_amount * 0.65
        )

        draw_open_mouth(
            surface,
            x,
            y,
            openness,
            smile
        )

        return


    # ========================================================
    # 2. SURPRISE / BOUCHE OUVERTE
    # ========================================================

    if mouth_open > 0.20:

        draw_open_mouth(
            surface,
            x,
            y,
            mouth_open,
            smile
        )

        return


    # ========================================================
    # 3. HEUREUX
    # ========================================================

    if smile > 0.08:

        draw_happy_mouth(
            surface,
            x,
            y,
            smile
        )

        return


    # ========================================================
    # 4. TRISTE
    # ========================================================

    if smile < -0.08:

        draw_sad_mouth(
            surface,
            x,
            y,
            abs(smile)
        )

        return


    # ========================================================
    # 5. NEUTRE
    # ========================================================

    draw_neutral_mouth(
        surface,
        x,
        y
    )