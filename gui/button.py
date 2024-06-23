import pygame


class Button:
    def __init__(self, text, position, size, celestial_body, indent_level, color=(255, 255, 255), border_color=(0, 0, 0), border_width=2):
        self.text = text
        self.position = position
        self.size = size
        self.celestial_body = celestial_body
        self.indent_level = indent_level
        self.color = color
        self.border_color = border_color
        self.border_width = border_width

    def draw(self, surface):
        # Adjust the x-coordinate of the button's position based on its level of indentation
        position = (self.position[0] + self.indent_level * 10, self.position[1])
        # Draw the button (border)
        pygame.draw.rect(surface, self.border_color, pygame.Rect(position, self.size))
        # Draw another rectangle inside the button for the inner color
        inner_pos = (position[0] + self.border_width, position[1] + self.border_width)
        inner_size = (self.size[0] - 2 * self.border_width, self.size[1] - 2 * self.border_width)
        pygame.draw.rect(surface, self.color, pygame.Rect(inner_pos, inner_size))
        # Render the text
        font = pygame.font.Font(None, 24)
        text = font.render(self.text, True, (0, 0, 0))
        surface.blit(text, (position[0] + 10, position[1] + 10))

    def is_clicked(self, mouse_pos, event, gui_manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                x, y = mouse_pos
                if self.position[0] <= x <= self.position[0] + self.size[0] and self.position[1] <= y <= self.position[1] + self.size[1]:
                    gui_manager.target_body = self.celestial_body
                    return True
        return False
