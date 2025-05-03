import pygame
import os

# Khởi tạo
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Tải tất cả frame
frames = []
for i in range(6):
    path = os.path.join("sprites","fight3", f"frame_{i}.png")
    img = pygame.image.load(path).convert_alpha()
    frames.append(img)

# Cấu hình animation
frame_index = 0
animation_speed = 150  # ms
timer = 0

# Vòng lặp game
running = True
while running:
    dt = clock.tick(60)  # giới hạn 60 FPS
    timer += dt

    # Xử lý sự kiện thoát
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Đổi frame khi đến thời gian
    if timer >= animation_speed:
        frame_index = (frame_index + 1) % len(frames)
        timer = 0

    # Vẽ
    screen.fill((0, 0, 0))
    screen.blit(frames[frame_index], (100, 100))
    pygame.display.flip()

pygame.quit()
input("nhan enter...")
