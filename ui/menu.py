import pygame
from ui.button import Button
from utils.support import import_image
from os.path import join
from ui.button import Button

class Menu:
    def __init__(self, surface):
        self.display_surface = surface
        self.font = {
            'btn': pygame.font.Font(join('assets', 'font', 'PixelifySans.ttf'), 50),
            'title': pygame.font.Font(join('assets', 'font', 'PixelifySans.ttf'), 70)
        }
        # Load background
        self.bg_image = import_image(join('assets', 'sprites', 'menu', 'bg'))  # Đặt hình nền menu tại: assets/menu_bg.png

        # Load buttons
        title_img = import_image(join('assets', 'sprites', 'menu', 'banner'))
        start_img = import_image(join('assets', 'sprites', 'menu', 'button2'))
        exit_img = import_image(join('assets', 'sprites', 'menu', 'button2'))
        music_img = import_image(join('assets', 'sprites', 'menu', 'button2'))
        self.title_button = Button(title_img, pos = (self.display_surface.get_rect().centerx, 180), text_input = "HUNTER", font = self.font['title'], base_color = "#000000", hovering_color = "#000000")  # chỉnh lại toạ độ tuỳ theo ảnh
        self.start_button = Button(start_img, pos = (self.display_surface.get_rect().centerx, 350), text_input = "PLAY", font = self.font['btn'], base_color = "#000000", hovering_color = "#283FC1")  # chỉnh lại toạ độ tuỳ theo ảnh
        self.exit_button = Button(exit_img, pos = (self.display_surface.get_rect().centerx, 500), text_input = "QUIT", font = self.font['btn'], base_color = "#000000", hovering_color = "#283FC1")
        self.music_button = Button(exit_img, pos = (self.display_surface.get_rect().centerx, 650), text_input = "MUSIC OFF", font = self.font['btn'], base_color = "#000000", hovering_color = "#283FC1")
    def run(self):
        # Vẽ nền
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.display_surface.get_width(), self.display_surface.get_height()))
        self.display_surface.blit(self.bg_image, (0, 0))

        for button in [self.title_button, self.start_button, self.exit_button, self.music_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self.display_surface)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.checkForInput(MENU_MOUSE_POS):
                    return "play"
                if self.exit_button.checkForInput(MENU_MOUSE_POS):
                    return "quit"
                if self.music_button.checkForInput(MENU_MOUSE_POS):
                    if self.music_button.text_input == "MUSIC OFF":
                        self.music_button.turnon()
                        return "musicon"
                    else:
                        self.music_button.turnoff()
                        return "musicoff"
        
