
import pygame
import sys
import threading
import queue
import time

from face.face_engine import FaceEngine
from brain.llm import VisageLLM
from speech.tts import VisageTTS
from speech.stt import VisageSTT
from agents.smart_router import SmartAgentRouter
from vision.vision_agent import VisionAgent


# ============================================================
# INITIALISATION
# ============================================================

pygame.init()

WIDTH = 900
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "VISAGE-AI | Assistant vocal intelligent + Agents IA + Vision"
)

clock = pygame.time.Clock()

face = FaceEngine(WIDTH, HEIGHT)
llm = VisageLLM()
tts = VisageTTS()
router = SmartAgentRouter()

stt = None

# ============================================================
# VISION AGENT
# ============================================================

vision = VisionAgent(camera_index=0)
vision_enabled = vision.start()

face.set_vision_enabled(vision_enabled)

# ============================================================
# ETATS
# ============================================================

auto_mode = True

is_listening = False
is_thinking = False
is_loading_stt = False

stop_listening = threading.Event()
resume_at = time.monotonic() + 1.0

result_queue = queue.Queue()

input_text = ""
last_message = ""
ai_response = "Bonjour ! Je suis VISAGE-AI."

current_emotion = "neutral"
current_intensity = 1.0
active_agent = "Aucun"

running = True
was_speaking = False

# ============================================================
# INTERFACE
# ============================================================

font = pygame.font.SysFont("arial", 21)
small_font = pygame.font.SysFont("arial", 17)

INPUT_RECT = pygame.Rect(
    30, HEIGHT - 65, WIDTH - 60, 45
)


# ============================================================
# GEMINI
# ============================================================

def ask_gemini(message):
    try:
        result = llm.analyze(message)
        result_queue.put(("success", result))
    except Exception as e:
        result_queue.put(("error", str(e)))


# ============================================================
# AGENTS IA
# ============================================================

def execute_agent(message):
    try:
        result = router.execute(message)

        if result is None:
            result = {"handled": False}

        if result.get("handled", False):
            result_queue.put(("agent_success", result))
        else:
            result_queue.put(("agent_not_handled", message))

    except Exception as e:
        result_queue.put(("agent_error", str(e)))


# ============================================================
# WHISPER
# ============================================================

def listen_microphone():
    global stt

    try:
        if stt is None:
            result_queue.put(("stt_loading", None))
            stt = VisageSTT()

        text = stt.listen_auto(
            stop_event=stop_listening,
            start_timeout=10,
            silence_duration=0.9,
            max_duration=15
        )

        result_queue.put(("transcription", text))

    except Exception as e:
        result_queue.put(("stt_error", str(e)))


def start_listening():
    global is_listening

    if (
        is_listening
        or is_thinking
        or tts.speaking
        or not auto_mode
        or input_text.strip()
    ):
        return

    stop_listening.clear()
    is_listening = True

    threading.Thread(
        target=listen_microphone,
        daemon=True
    ).start()


# ============================================================
# ENVOYER UNE COMMANDE
# ============================================================

def submit_message(message):
    global last_message
    global ai_response
    global is_thinking
    global resume_at
    global active_agent

    message = message.strip()

    if not message:
        return

    if is_thinking or is_listening or tts.speaking:
        return

    last_message = message
    is_thinking = True
    resume_at = float("inf")

    ai_response = "VISAGE-AI analyse votre demande..."
    active_agent = "Orchestrateur"

    face.set_emotion("thinking", 1.0)

    threading.Thread(
        target=execute_agent,
        args=(message,),
        daemon=True
    ).start()


# ============================================================
# REPONSE VOCALE
# ============================================================

def speak_response(response):
    global resume_at

    if response.strip():
        started = tts.speak_async(response)

        if not started:
            resume_at = time.monotonic() + 1.0
    else:
        resume_at = time.monotonic() + 1.0


# ============================================================
# TEXTE MULTILIGNE
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
    words = str(text).split()

    lines = []
    current_line = ""

    for word in words:
        candidate = f"{current_line} {word}".strip()

        if font_obj.size(candidate)[0] <= max_width:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    for index, line in enumerate(lines[:max_lines]):
        rendered = font_obj.render(
            line, True, color
        )
        surface.blit(
            rendered,
            (x, y + index * 23)
        )


# ============================================================
# BOUCLE PRINCIPALE
# ============================================================

try:
    while running:
        dt = clock.tick(FPS) / 1000.0

        # ====================================================
        # EVENEMENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                # F2 : MODE VOCAL AUTOMATIQUE
                elif event.key == pygame.K_F2:
                    auto_mode = not auto_mode

                    if not auto_mode:
                        stop_listening.set()
                        resume_at = float("inf")
                        ai_response = (
                            "Mode vocal automatique désactivé."
                        )
                    else:
                        resume_at = time.monotonic() + 0.5
                        ai_response = (
                            "Mode vocal automatique activé."
                        )

                    print(
                        "[VOCAL] Mode automatique :",
                        auto_mode
                    )

                # F4 : ACTIVER / DESACTIVER LA CAMERA
                elif event.key == pygame.K_F4:

                    if vision_enabled:
                        vision.stop()
                        vision_enabled = False
                        face.set_vision_enabled(False)
                        face.set_vision_position(False)

                        ai_response = (
                            "VisionAgent désactivé. "
                            "Les yeux suivent la souris."
                        )

                        print("[VISION] Mode souris.")

                    else:
                        vision_enabled = vision.start()
                        face.set_vision_enabled(
                            vision_enabled
                        )

                        if vision_enabled:
                            ai_response = (
                                "VisionAgent activé. "
                                "Les yeux suivent votre visage."
                            )
                        else:
                            ai_response = (
                                "Impossible d'activer VisionAgent. "
                                "Vérifiez la caméra et le modèle."
                            )

                        print(
                            "[VISION] Mode webcam :",
                            vision_enabled
                        )

                # ENTREE : ENVOYER LE MESSAGE
                elif event.key == pygame.K_RETURN:

                    if (
                        input_text.strip()
                        and not is_thinking
                        and not is_listening
                        and not tts.speaking
                    ):
                        message = input_text.strip()
                        input_text = ""
                        submit_message(message)

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]

                else:
                    if (
                        event.unicode
                        and event.unicode.isprintable()
                        and not is_listening
                    ):
                        if len(input_text) < 1000:
                            input_text += event.unicode

        # ====================================================
        # RESULTATS ASYNCHRONES
        # ====================================================

        while True:
            try:
                status, result = result_queue.get_nowait()
            except queue.Empty:
                break

            # CHARGEMENT WHISPER
            if status == "stt_loading":
                is_loading_stt = True
                ai_response = "Chargement de Whisper..."

            # TRANSCRIPTION
            elif status == "transcription":
                is_listening = False
                is_loading_stt = False

                recognized_text = (
                    str(result).strip()
                    if result is not None
                    else ""
                )

                if recognized_text:
                    print("\nVous :", recognized_text)
                    submit_message(recognized_text)
                else:
                    resume_at = time.monotonic() + 0.4

            # ERREUR MICROPHONE
            elif status == "stt_error":
                is_listening = False
                is_loading_stt = False

                ai_response = (
                    f"Erreur microphone : {result}"
                )

                print(ai_response)

                auto_mode = False
                resume_at = float("inf")

            # AGENT : COMMANDE EXECUTEE
            elif status == "agent_success":
                is_thinking = False

                active_agent = result.get(
                    "agent", "Agent IA"
                )

                current_emotion = result.get(
                    "emotion", "happy"
                )

                current_intensity = 0.8

                ai_response = str(
                    result.get(
                        "response",
                        "Commande exécutée."
                    )
                )

                face.set_emotion(
                    current_emotion,
                    current_intensity
                )

                print("\nAGENT :", active_agent)
                print("REPONSE :", ai_response)

                speak_response(ai_response)

            # AGENT NON RECONNU : GEMINI
            elif status == "agent_not_handled":
                active_agent = "Gemini"
                ai_response = "VISAGE-AI réfléchit..."

                threading.Thread(
                    target=ask_gemini,
                    args=(result,),
                    daemon=True
                ).start()

            # ERREUR AGENT
            elif status == "agent_error":
                is_thinking = False
                active_agent = "Agent IA"

                current_emotion = "sad"
                current_intensity = 0.7

                ai_response = (
                    "Impossible d'exécuter la commande : "
                    f"{result}"
                )

                face.set_emotion(
                    current_emotion,
                    current_intensity
                )

                print(ai_response)

                speak_response(
                    "Désolé, je n'ai pas pu "
                    "exécuter cette commande."
                )

            # REPONSE GEMINI
            elif status == "success":
                is_thinking = False

                if not isinstance(result, dict):
                    result = {
                        "emotion": "neutral",
                        "intensity": 1.0,
                        "response": str(result)
                    }

                current_emotion = result.get(
                    "emotion", "neutral"
                )

                try:
                    current_intensity = float(
                        result.get("intensity", 1.0)
                    )
                except (ValueError, TypeError):
                    current_intensity = 1.0

                current_intensity = max(
                    0.0,
                    min(1.0, current_intensity)
                )

                ai_response = str(
                    result.get("response", "")
                )

                face.set_emotion(
                    current_emotion,
                    current_intensity
                )

                print(
                    "\nEMOTION :",
                    current_emotion
                )
                print("REPONSE :", ai_response)

                speak_response(ai_response)

            # ERREUR GEMINI
            elif status == "error":
                is_thinking = False
                active_agent = "Gemini"

                current_emotion = "neutral"
                current_intensity = 1.0

                ai_response = (
                    f"Erreur Gemini : {result}"
                )

                face.set_emotion("neutral", 1.0)

                print(ai_response)
                resume_at = time.monotonic() + 1.0

        # ====================================================
        # FIN DE LA REPONSE VOCALE
        # ====================================================

        if was_speaking and not tts.speaking:
            resume_at = time.monotonic() + 1.0

            face.set_emotion(
                current_emotion,
                current_intensity
            )

        was_speaking = tts.speaking

        # ====================================================
        # ECOUTE AUTOMATIQUE
        # ====================================================

        if (
            auto_mode
            and not is_listening
            and not is_thinking
            and not tts.speaking
            and not input_text.strip()
            and time.monotonic() >= resume_at
        ):
            start_listening()

        # ====================================================
        # ANIMATION DE LA BOUCHE
        # ====================================================

        if tts.speaking:
            if face.emotion != "talking":
                face.set_emotion("talking", 0.65)

        # ====================================================
        # VISION : SUIVI DU VISAGE
        # ====================================================

        if vision_enabled:
            detected, vx, vy = (
                vision.get_face_position()
            )

            face.set_vision_position(
                detected, vx, vy
            )

        else:
            detected = False
            face.set_vision_position(False)

        # ====================================================
        # ANIMATIONS
        # ====================================================

        face.update(dt)
        face.draw(screen)

        # ====================================================
        # PANNEAU CONVERSATION
        # ====================================================

        panel = pygame.Rect(
            25, 15, WIDTH - 50, 155
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

        vision_status = (
            "Visage détecté"
            if vision_enabled and detected
            else "Recherche..."
            if vision_enabled
            else "OFF"
        )

        title = small_font.render(
            (
                f"VISAGE-AI | Emotion : {current_emotion}"
                f" | Agent : {active_agent}"
            ),
            True,
            (0, 220, 235)
        )

        screen.blit(title, (40, 25))

        vision_label = small_font.render(
            f"Vision : {vision_status} | F4 : caméra",
            True,
            (0, 200, 220)
        )

        screen.blit(
            vision_label,
            (40, 47)
        )

        draw_wrapped_text(
            screen,
            (
                f"Vous : {last_message}"
                if last_message
                else "Vous : ..."
            ),
            40,
            75,
            WIDTH - 85,
            (190, 210, 225),
            small_font,
            max_lines=1
        )

        draw_wrapped_text(
            screen,
            f"VISAGE : {ai_response}",
            40,
            110,
            WIDTH - 85,
            (235, 245, 255),
            small_font,
            max_lines=2
        )

        # ====================================================
        # ZONE DE SAISIE
        # ====================================================

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
            visible_text = visible_text[1:]

        if not visible_text:
            visible_text = (
                "F2 : vocal | F4 : caméra | "
                "Entrée : envoyer du texte..."
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

        # ====================================================
        # INDICATEUR D'ETAT
        # ====================================================

        if is_loading_stt:
            indicator_text = "CHARGEMENT WHISPER"
            indicator_color = (255, 205, 80)

        elif is_listening:
            indicator_text = "MICROPHONE ACTIF"
            indicator_color = (255, 90, 90)

        elif is_thinking:
            indicator_text = (
                f"AGENT ACTIF : {active_agent.upper()}"
            )
            indicator_color = (255, 205, 80)

        elif tts.speaking:
            indicator_text = "VISAGE-AI PARLE"
            indicator_color = (0, 225, 180)

        elif auto_mode:
            indicator_text = "MODE VOCAL AUTOMATIQUE"
            indicator_color = (0, 200, 220)

        else:
            indicator_text = (
                "MODE CLAVIER | F2 POUR PARLER"
            )
            indicator_color = (170, 190, 210)

        indicator = small_font.render(
            indicator_text,
            True,
            indicator_color
        )

        indicator_rect = indicator.get_rect(
            center=(WIDTH // 2, HEIGHT - 90)
        )

        screen.blit(indicator, indicator_rect)

        pygame.display.flip()

finally:
    # ========================================================
    # FERMETURE
    # ========================================================

    stop_listening.set()
    vision.stop()
    pygame.quit()

sys.exit()
