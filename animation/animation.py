import pygame
import os

class Animation:
    def __init__(self, folder_path, frame_duration=100):
        self.frames = []
        self.load_frames(folder_path)
        self.frame_duration = frame_duration
        self.current_time = 0
        self.current_frame = 0

    def load_frames(self, folder_path):
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename))
                self.frames.append(img)

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.frame_duration:
            self.current_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_frame(self):
        return self.frames[self.current_frame]
