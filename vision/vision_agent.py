
import threading
import time
from pathlib import Path

import cv2
import mediapipe as mp


class VisionAgent:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index

        self.face_detected = False
        self.face_x = 0.0
        self.face_y = 0.0

        self.running = False
        self.thread = None
        self.lock = threading.Lock()

        self.model_path = (
            Path(__file__).resolve().parent
            / "blaze_face_short_range.tflite"
        )

    def start(self):
        if self.thread is not None and self.thread.is_alive():
            return False

        if not self.model_path.exists():
            print("[VISION] Modele MediaPipe introuvable.")
            print("[VISION] Chemin :", self.model_path)
            return False

        with self.lock:
            self.face_detected = False

        self.running = True
        self.thread = threading.Thread(
            target=self._camera_loop,
            daemon=True,
            name="VisionAgent"
        )
        self.thread.start()

        print("[VISION] Demarrage de VisionAgent...")
        return True

    def _camera_loop(self):
        camera = None

        try:
            camera = cv2.VideoCapture(
                self.camera_index,
                cv2.CAP_DSHOW
            )

            if not camera.isOpened():
                camera.release()
                camera = cv2.VideoCapture(self.camera_index)

            if not camera.isOpened():
                print("[VISION] Webcam inaccessible.")
                return

            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            options = mp.tasks.vision.FaceDetectorOptions(
                base_options=mp.tasks.BaseOptions(
                    model_asset_path=str(self.model_path)
                ),
                running_mode=mp.tasks.vision.RunningMode.IMAGE,
                min_detection_confidence=0.5
            )

            detector_class = mp.tasks.vision.FaceDetector

            with detector_class.create_from_options(
                options
            ) as detector:

                print("[VISION] Camera active.")

                while self.running:
                    success, frame = camera.read()

                    if not success:
                        with self.lock:
                            self.face_detected = False
                        time.sleep(0.1)
                        continue

                    frame = cv2.flip(frame, 1)
                    height, width = frame.shape[:2]

                    rgb = cv2.cvtColor(
                        frame,
                        cv2.COLOR_BGR2RGB
                    )

                    image = mp.Image(
                        image_format=mp.ImageFormat.SRGB,
                        data=rgb
                    )

                    result = detector.detect(image)

                    if result.detections:
                        detection = max(
                            result.detections,
                            key=lambda d: (
                                d.categories[0].score
                                if d.categories else 0.0
                            )
                        )

                        box = detection.bounding_box

                        center_x = (
                            box.origin_x + box.width / 2.0
                        )
                        center_y = (
                            box.origin_y + box.height / 2.0
                        )

                        x = max(
                            -1.0,
                            min(1.0, 2.0 * center_x / width - 1.0)
                        )

                        y = max(
                            -1.0,
                            min(1.0, 2.0 * center_y / height - 1.0)
                        )

                        with self.lock:
                            self.face_detected = True
                            self.face_x = x
                            self.face_y = y
                    else:
                        with self.lock:
                            self.face_detected = False

        except Exception as error:
            print("[VISION] Erreur :", error)

        finally:
            if camera is not None:
                camera.release()

            with self.lock:
                self.face_detected = False

            self.running = False
            print("[VISION] Camera fermee.")

    def get_face_position(self):
        with self.lock:
            return (
                self.face_detected,
                self.face_x,
                self.face_y
            )

    def stop(self):
        self.running = False

        if (
            self.thread is not None
            and self.thread.is_alive()
            and threading.current_thread() is not self.thread
        ):
            self.thread.join(timeout=3.0)

        with self.lock:
            self.face_detected = False

        print("[VISION] Arret demande.")
