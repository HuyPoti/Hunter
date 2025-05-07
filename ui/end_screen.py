import pygame
from ui.button import Button
from utils.support import import_image
from os.path import join

class EndScreen:
    def __init__(self, surface, result):
        self.display_surface = surface
        self.result = result  # "win" hoặc "lose"

        # Font
        self.font = {
            'title': pygame.font.Font(join('assets', 'font', 'PixelifySans.ttf'), 70),
            'btn': pygame.font.Font(join('assets', 'font', 'PixelifySans.ttf'), 50)
        }

        # Background
        self.bg_image = import_image(join('assets', 'sprites', 'menu', 'bg'))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.display_surface.get_width(), self.display_surface.get_height()))
        # Buttons
        title_img = import_image(join('assets', 'sprites', 'menu', 'banner'))
        button_img = import_image(join('assets', 'sprites', 'menu', 'button2'))
        self.title_button = Button(title_img, pos = (self.display_surface.get_rect().centerx, 150), text_input = "HUNTER", font = self.font['title'], base_color = "#000000", hovering_color = "#000000")  # chỉnh lại toạ độ tuỳ theo ảnh
        self.play_again_button = Button(button_img, pos=(self.display_surface.get_rect().centerx, 400), text_input="HOME", font=self.font['btn'], base_color=(0, 0, 0), hovering_color=(40, 63, 193))
        self.quit_button = Button(button_img, pos=(self.display_surface.get_rect().centerx, 550), text_input="QUIT", font=self.font['btn'], base_color=(0, 0, 0), hovering_color=(40, 63, 193))

    def run(self):
        # Lấy vị trí chuột
        mouse_pos = pygame.mouse.get_pos()

        # Vẽ nền
        self.display_surface.blit(self.bg_image, (0, 0))

        # Hiển thị thông báo
        if self.result == "win":
            text = self.font['title'].render("YOU WIN!", True, (0, 255, 0))
        else:
            text = self.font['title'].render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.display_surface.get_rect().centerx, 300))
        self.display_surface.blit(text, text_rect)

        # Vẽ các nút
        for button in [self.play_again_button, self.quit_button, self.title_button]:
            button.changeColor(mouse_pos)
            button.update(self.display_surface)

        # Xử lý sự kiện
        for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_again_button.checkForInput(mouse_pos):
                    return "play_again"
                if self.quit_button.checkForInput(mouse_pos):
                    return "quit"

        return None