import numpy as np
import pygame
from OpenGL.GL import *

from gui.button import Button


def get_indent_level(celestial_body):
    level = 0
    while celestial_body.parent_body is not None:
        level += 1
        celestial_body = celestial_body.parent_body
    return level


class DropdownMenu:
    def __init__(self, celestial_bodies, gui_manager):
        self.celestial_bodies = celestial_bodies
        self.gui_manager = gui_manager
        self.open = False
        self.buttons = [Button(body.p_name, (20, 20 + i * 30), (160, 30), body, get_indent_level(body)) for i, body
                        in enumerate(celestial_bodies)]
        self.scroll_offset = 0

    def draw(self):
        menu_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        menu_surface.fill((150, 150, 150, 128))  # Add transparency to the menu
        pygame.draw.rect(menu_surface, (0, 0, 0), menu_surface.get_rect(), 2)  # Draw a border
        for i, button in enumerate(self.buttons[self.scroll_offset:]):
            button.position = (20, 20 + i * 30)  # Update button position based on scroll offset
            button.draw(menu_surface)

        tex_id = self.create_texture_from_surface(menu_surface)
        return tex_id

    def handle_scroll(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.button == 5:  # Scroll down
                self.scroll_offset = min(len(self.buttons) - 1, self.scroll_offset + 1)

    def handle_event(self, event):
        if self.open:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_clicked(mouse_pos, event, self.gui_manager):
                    break
            self.handle_scroll(event)

    @staticmethod
    def create_texture_from_surface(surface):
        surface = pygame.transform.flip(surface, True, True)
        texture_data = pygame.image.tostring(surface, 'RGBA', 1)
        width, height = surface.get_size()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return tex_id
