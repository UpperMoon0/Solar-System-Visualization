from OpenGL.GL import *
from OpenGL.GLU import *

from model.orbit import Orbit


class CelestialBody:
    def __init__(self, b_name, radius, color, orbit_radius=0, orbit_speed=0, parent_body=None):
        self.name = b_name
        self.radius = radius
        self.color = color
        self.position = (0, 0, 0)
        self.orbit = Orbit(orbit_radius, orbit_speed, parent_body)

    def draw(self):
        glColor3fv(self.color)
        quad = gluNewQuadric()
        glPushMatrix()
        glTranslatef(*self.position)
        gluSphere(quad, self.radius, 32, 32)
        glPopMatrix()

    def update_position(self):
        self.position = self.orbit.update_position()

    def draw_orbit(self):
        self.orbit.draw_orbit()
