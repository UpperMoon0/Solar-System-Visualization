import math

from OpenGL.GL import *
from OpenGL.GLU import *


class CelestialBody:
    def __init__(self, radius, color, orbit_radius=0, orbit_speed=0):
        self.radius = radius
        self.color = color
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.angle = 0

    def draw(self):
        glColor3fv(self.color)
        quad = gluNewQuadric()
        gluSphere(quad, self.radius, 32, 32)

    def update_position(self):
        self.angle += self.orbit_speed

    def draw_orbit(self):
        glColor3f(1, 1, 1)
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            angle = math.radians(float(i) / 100 * 360.0)
            orbit_x = self.orbit_radius * math.cos(angle)
            orbit_z = self.orbit_radius * math.sin(angle)
            glVertex3f(orbit_x, 0, orbit_z)
        glEnd()
