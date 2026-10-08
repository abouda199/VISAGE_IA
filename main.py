
import pygame
import sys
import threading
import queue

from face.face_engine import FaceEngine
from brain.llm import VisageLLM
from speech.tts import VisageTTS


# ============================================================
# INITIALISATION
# ============================================================

pygame.init()

WIDTH = 900
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "VISAGE-AI | Assistant vocal intelligent"
)

clock = pygame.time.Clock()

face = FaceEngine(WIDTH, HEIGHT)
llm = VisageLLM()
tts = VisageTTS()

# ============================================================
# INTERFACE
# ============================================================

font = pygame.font.SysFont("arial", 21)
small_font = pygame.font.SysFont("arial", 17)

input_text = ""
last_message = ""

ai_response = (
    "Bonjour ! Je suis VISAGE-AI."
)

current_emotion = "neutral"

is_thinking = False

result_queue = queue.Queue()

INPUT_RECT = pygame.Rect(
    30,
    HEIGHT - 65,
    WIDTH - 60,
    45
)


# ============================================================
# APPEL GEMINI
# ============================================================

def ask_gemini(message):

    try:

        result = llm.analyze(message)

        result_queue.put(
            ("success", result)
        )

    except Exception as e:

        result_queue.put(
            ("error", str(e))
        )


# ============================================================
# AFFICHAGE TEXTE
# ============================================================

def draw_wrapped_text(
    surface,
    text,
    x,
    y,
    max_width,
    color,
    font_obj,
    max_lines=3
):

    words = text.split()

    lines = []
    current_line = ""

    for word in words:

        candidate = (
            f"{current_line} {word}".strip()
        )

        if (
            font_obj.size(candidate)[0]
            <= max_width
        ):

            current_line = candidate

        else:

            if current_line:
                lines.append(current_line)

            current_line = word

    if current_line:
        lines.append(current_line)

    for index, line in enumerate(
        lines[:max_lines]
    ):

        rendered = font_obj.render(
            line,
            True,
            color
        )

        surface.blit(
            rendered,
            (x, y + index * 23)
        )


# ============================================================
# BOUCLE PRINCIPALE
# ============================================================

running = True

while running:

    dt = clock.tick(FPS) / 1000.0

    # ========================================================
    # EVENEMENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_RETURN:

                if (
                    input_text.strip()
                    and not is_thinking
                ):

                    last_message = (
                        input_text.strip()
                    )

                    input_text = ""

                    is_thinking = True

                    ai_response = (
                        "VISAGE-AI réfléchit..."
                    )

                    face.set_emotion(
                        "thinking",
                        1.0
                    )

                    worker = threading.Thread(
                        target=ask_gemini,
                        args=(last_message,),
                        daemon=True
                    )

                    worker.start()

            elif event.key == pygame.K_BACKSPACE:

                input_text = input_text[:-1]

            else:

                if (
                    event.unicode
                    and event.unicode.isprintable()
                ):

                    if len(input_text) < 1000:
                        input_text += event.unicode

    # ========================================================
    # REPONSE GEMINI
    # ========================================================

    try:

        status, result = (
            result_queue.get_nowait()
        )

        is_thinking = False

        if status == "success":

            current_emotion = (
                result["emotion"]
            )

            intensity = (
                result["intensity"]
            )

            ai_response = (
                result["response"]
            )

            face.set_emotion(
                current_emotion,
                intensity
            )

            print(
                "\nMESSAGE :", last_message
            )

            print(
                "EMOTION :", current_emotion
            )

            print(
                "INTENSITE :", intensity
            )

            print(
                "REPONSE :", ai_response
            )

            # ================================================
            # VOIX FEMININE FRANCAISE
            # ================================================

            tts.speak_async(
                ai_response
            )

        else:

            current_emotion = "neutral"

            ai_response = (
                f"Erreur Gemini : {result}"
            )

            face.set_emotion(
                "neutral"
            )

            print(ai_response)

    except queue.Empty:
        pass

    # ========================================================
    # ANIMATION DE LA BOUCHE
    # ========================================================

    if tts.speaking:

        if face.emotion != "talking":

            face.set_emotion(
                "talking",
                0.65
            )

    else:

        if (
            face.emotion == "talking"
        ):

            face.set_emotion(
                current_emotion,
                1.0
            )

    # ========================================================
    # ANIMATIONS
    # ========================================================

    face.update(dt)
    face.draw(screen)

    # ========================================================
    # PANNEAU DE CONVERSATION
    # ========================================================

    panel = pygame.Rect(
        25,
        15,
        WIDTH - 50,
        155
    )

    pygame.draw.rect(
        screen,
        (17, 27, 42),
        panel,
        border_radius=14
    )

    pygame.draw.rect(
        screen,
        (0, 165, 195),
        panel,
        width=1,
        border_radius=14
    )

    title = small_font.render(
        f"VISAGE-AI | Emotion : {current_emotion}",
        True,
        (0, 220, 235)
    )

    screen.blit(
        title,
        (40, 25)
    )

    draw_wrapped_text(
        screen,
        (
            f"Vous : {last_message}"
            if last_message
            else "Vous : ..."
        ),
        40,
        55,
        WIDTH - 85,
        (190, 210, 225),
        small_font,
        max_lines=2
    )

    draw_wrapped_text(
        screen,
        f"VISAGE : {ai_response}",
        40,
        105,
        WIDTH - 85,
        (235, 245, 255),
        small_font,
        max_lines=2
    )

    # ========================================================
    # ZONE DE SAISIE
    # ========================================================

    pygame.draw.rect(
        screen,
        (18, 25, 38),
        INPUT_RECT,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        (0, 210, 230),
        INPUT_RECT,
        width=2,
        border_radius=10
    )

    visible_text = input_text

    while (
        visible_text
        and font.size(visible_text)[0]
        > INPUT_RECT.width - 25
    ):

        visible_text = (
            visible_text[1:]
        )

    if not visible_text:

        visible_text = (
            "Ecrivez un message puis appuyez sur Entree..."
        )

        color = (115, 135, 155)

    else:

        color = (235, 245, 255)

    rendered = font.render(
        visible_text,
        True,
        color
    )

    screen.blit(
        rendered,
        (
            INPUT_RECT.x + 12,
            INPUT_RECT.y + 10
        )
    )

    # ========================================================
    # AFFICHAGE
    # ========================================================

    pygame.display.flip()


pygame.quit()
sys.exit()
