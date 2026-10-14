
import cv2
import mediapipe as mp

# ==================================================
# VISAGE-AI - ETAPE 2 : DETECTION DU VISAGE
# ==================================================

def main():
    print("[VISION] Initialisation de la webcam...")

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        camera.release()
        camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("[ERREUR] Webcam introuvable.")
        return

    # MediaPipe Tasks API
    # Le modele sera telecharge automatiquement
    # si le fichier n'existe pas.
    from pathlib import Path
    from urllib.request import urlretrieve

    model_path = Path(__file__).parent / "blaze_face_short_range.tflite"

    if not model_path.exists():
        print("[VISION] Telechargement du modele MediaPipe...")
        url = (
            "https://storage.googleapis.com/mediapipe-models/"
            "face_detector/blaze_face_short_range/float16/1/"
            "blaze_face_short_range.tflite"
        )
        try:
            urlretrieve(url, str(model_path))
        except Exception as error:
            print("[ERREUR] Telechargement du modele :", error)
            camera.release()
            return

    BaseOptions = mp.tasks.BaseOptions
    FaceDetector = mp.tasks.vision.FaceDetector
    FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
    RunningMode = mp.tasks.vision.RunningMode

    options = FaceDetectorOptions(
        base_options=BaseOptions(
            model_asset_path=str(model_path)
        ),
        running_mode=RunningMode.IMAGE,
        min_detection_confidence=0.5,
    )

    print("[VISION] Detection active. Appuie sur Q pour quitter.")

    try:
        with FaceDetector.create_from_options(options) as detector:
            while True:
                success, frame = camera.read()

                if not success:
                    print("[ERREUR] Lecture camera impossible.")
                    break

                frame = cv2.flip(frame, 1)
                height, width = frame.shape[:2]

                rgb_frame = cv2.cvtColor(
                    frame, cv2.COLOR_BGR2RGB
                )

                mp_image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb_frame
                )

                result = detector.detect(mp_image)

                if result.detections:
                    # Garder la detection la plus confiante
                    detection = max(
                        result.detections,
                        key=lambda d: d.categories[0].score
                        if d.categories else 0
                    )

                    box = detection.bounding_box

                    x1 = max(0, box.origin_x)
                    y1 = max(0, box.origin_y)
                    x2 = min(width - 1, box.origin_x + box.width)
                    y2 = min(height - 1, box.origin_y + box.height)

                    # Centre du visage
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2

                    # Coordonnees normalisees entre -1 et +1
                    norm_x = (center_x / width) * 2 - 1
                    norm_y = (center_y / height) * 2 - 1

                    # Rectangle cyan
                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (255, 255, 0),
                        2
                    )

                    # Centre du visage
                    cv2.circle(
                        frame,
                        (int(center_x), int(center_y)),
                        5,
                        (0, 255, 255),
                        -1
                    )

                    cv2.putText(
                        frame,
                        f"FACE DETECTED | X={norm_x:+.2f} Y={norm_y:+.2f}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 255, 0),
                        2
                    )

                else:
                    cv2.putText(
                        frame,
                        "NO FACE DETECTED",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (0, 0, 255),
                        2
                    )

                cv2.imshow(
                    "VISAGE-AI | Face Detection",
                    frame
                )

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("[VISION] Camera fermee.")


if __name__ == "__main__":
    main()
