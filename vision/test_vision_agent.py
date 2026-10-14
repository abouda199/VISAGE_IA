
import time
from vision.vision_agent import VisionAgent


def main():
    vision = VisionAgent()

    vision.start()

    print("[TEST] Suivi du visage actif.")
    print("[TEST] Ctrl+C pour quitter.")

    try:
        while True:
            detected, x, y = vision.get_face_position()

            if detected:
                print(
                    f"\r[FACE] X={x:+.2f} | Y={y:+.2f}   ",
                    end="",
                    flush=True
                )
            else:
                print(
                    "\r[FACE] Aucun visage detecte.       ",
                    end="",
                    flush=True
                )

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n[TEST] Arret demande.")

    finally:
        vision.stop()


if __name__ == "__main__":
    main()

