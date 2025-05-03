import pygame
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

frames = []
for i in range(2):
    path = os.path.join("sprites", "attack" ,  f"frame_{i}.png")
    img = pygame.image.load(path).convert_alpha()
    frames.append(img) 

frame_index = 0
animation_speed = 150 
timer = 0

running = True
while running:
    dt = clock.tick(60)
    timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if timer >= animation_speed:
        frame_index = (frame_index + 1) % len(frames)
        timer = 0

    screen.fill((0, 0, 0))
    screen.blit(frames[frame_index], (100, 100))
    pygame.display.flip()

pygame.quit()
input("nhan enter...")
