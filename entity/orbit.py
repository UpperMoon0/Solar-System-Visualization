import math

from OpenGL.GL import *


class Orbit:
    def __init__(self, radius, speed, parent_body=None):
        self.radius = radius
        self.speed = speed
        self.angle = 0
        self.parent_body = parent_body

    def update_position(self):
        self.angle += self.speed
        parent_x, parent_y, parent_z = (0, 0, 0)
        if self.parent_body:
            parent_x, parent_y, parent_z = self.parent_body.position
        position = (
            parent_x + self.radius * math.cos(math.radians(self.angle)),
            parent_y,
            parent_z + self.radius * math.sin(math.radians(self.angle))
        )
        return position

    def draw_orbit(self):
        if self.radius > 0:
            glColor3f(1, 1, 1)
            glBegin(GL_LINE_LOOP)
            parent_x, parent_y, parent_z = (0, 0, 0)
            if self.parent_body:
                parent_x, parent_y, parent_z = self.parent_body.position
            for i in range(100):
                angle = math.radians(float(i) / 100 * 360.0)
                orbit_x = parent_x + self.radius * math.cos(angle)
                orbit_z = parent_z + self.radius * math.sin(angle)
                glVertex3f(orbit_x, 0, orbit_z)
            glEnd()
