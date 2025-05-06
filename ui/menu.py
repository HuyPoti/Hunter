import pygame
from ui.button import Button
from utils.support import import_image
from os.path import join

class Menu:
    def __init__(self, surface):
        self.display_surface = surface

        # Load background
        self.bg_image = import_image(join('assets', 'bg'))  # Đặt hình nền menu tại: assets/menu_bg.png

        # Load buttons
        start_img = import_image(join('assets', 'start_btn'))
        exit_img = import_image(join('assets', 'exit_btn'))

        self.start_button = Button(300, 250, start_img, 1)  # chỉnh lại toạ độ tuỳ theo ảnh
        self.exit_button = Button(300, 350, exit_img, 1)

    def run(self):
        # Vẽ nền
        self.display_surface.blit(self.bg_image, (0, 0))

        # Vẽ nút và xử lý nhấn
        if self.start_button.draw(self.display_surface):
            return "play"
        elif self.exit_button.draw(self.display_surface):
            return "quit"
        
        return None

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return "quit"
        return None
