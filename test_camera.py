
import cv2

print("[VISION] Ouverture de la webcam...")

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camera.isOpened():
    camera.release()
    camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("[ERREUR] Webcam introuvable.")
else:
    print("[VISION] Webcam active !")
    print("[VISION] Appuie sur Q pour quitter.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("[ERREUR] Lecture impossible.")
                break

            frame = cv2.flip(frame, 1)

            cv2.putText(
                frame,
                "VISAGE-AI | VisionAgent",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            cv2.imshow("VISAGE-AI - Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()

print("[VISION] Test termine.")
