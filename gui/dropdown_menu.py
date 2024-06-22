import numpy as np
import pygame
from OpenGL.GL import *

from gui.button import Button


class DropdownMenu:
    def __init__(self, celestial_bodies, gui_manager):
        self.celestial_bodies = celestial_bodies
        self.gui_manager = gui_manager
        self.open = False
        self.buttons = [Button(body.name, (20, 20 + i * 30), (160, 30), body) for i, body in enumerate(celestial_bodies)]

    def draw(self):
        menu_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        menu_surface.fill((150, 150, 150, 128))  # Add transparency to the menu
        pygame.draw.rect(menu_surface, (0, 0, 0), menu_surface.get_rect(), 2)  # Draw a border
        for button in self.buttons:
            button.draw(menu_surface)

        tex_id = self.create_texture_from_surface(menu_surface)
        return tex_id

    @staticmethod
    def create_texture_from_surface(surface):
        texture_data = pygame.surfarray.array3d(surface)
        texture_data = np.rot90(texture_data, -1)  # Rotate the texture data
        width, height = surface.get_size()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return tex_id

    def handle_event(self, event):
        if self.open:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(mouse_pos, event, self.gui_manager):
                    break
