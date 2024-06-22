from OpenGL.GL import *

from gui.dropdown_menu import DropdownMenu


class GuiManager:
    def __init__(self, celestial_bodies, display):
        self.target_body = celestial_bodies[0]
        self.dropdown_menu = DropdownMenu(celestial_bodies, self)
        self.display = display

    def switch_to_2d(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.display[0], self.display[1], 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

    def switch_to_3d(self):
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def draw(self):
        if self.dropdown_menu.open:
            self.switch_to_2d()
            texture_id = self.dropdown_menu.draw()
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glBegin(GL_QUADS)
            glTexCoord2f(1, 0)  # Flip the x-coordinate here
            glVertex2f(10, 10)
            glTexCoord2f(0, 0)  # And here
            glVertex2f(210, 10)
            glTexCoord2f(0, 1)  # And here
            glVertex2f(210, 210)
            glTexCoord2f(1, 1)  # And here
            glVertex2f(10, 210)
            glEnd()
            glDisable(GL_TEXTURE_2D)
            glDeleteTextures([texture_id])
            self.switch_to_3d()