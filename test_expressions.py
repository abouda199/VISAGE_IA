
import pygame
from face.face_engine import FaceEngine

pygame.init()

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("VISAGE-AI - Test expressions")

clock = pygame.time.Clock()
face = FaceEngine(900, 600)

emotions = {
    pygame.K_1: "neutral",
    pygame.K_2: "happy",
    pygame.K_3: "angry",
    pygame.K_4: "surprised",
    pygame.K_5: "wink",
    pygame.K_6: "excited",
    pygame.K_7: "love",
    pygame.K_8: "sleepy",
    pygame.K_9: "confused",
    pygame.K_0: "thinking",
}

running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key in emotions:
                emotion = emotions[event.key]
                face.set_emotion(emotion)
                print("Expression :", emotion)

    face.update(dt)
    face.draw(screen)
    pygame.display.flip()

pygame.quit()
