import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from physics import calculate_acceleration, update_position, update_velocity


class CelestialBody:
    def __init__(self,
                 p_name,
                 radius,
                 mass,
                 color,
                 initial_position=np.array([0, 0, 0]),
                 initial_velocity=np.array([0, 0, 0]),
                 initial_acceleration=np.array([0, 0, 0]),
                 parent_body=None):
        """
        Initialize a celestial body.

        Parameters:
        b_name (str): Name of the celestial body.
        radius (float): Radius of the celestial body (m).
        mass (float): Mass of the celestial body (kg).
        color (tuple): RGB color of the celestial body.
        initial_position (np.array, optional): Initial position vector of the celestial body (shape: [3]).
        initial_velocity (np.array, optional): Initial velocity vector of the celestial body (shape: [3]).
        initial_acceleration (np.array, optional): Initial acceleration vector of the celestial body (shape: [3]).
        parent_body (CelestialBody, optional): Parent body of the celestial body.
        """
        self.p_name = p_name
        self.radius = radius
        self.mass = mass
        self.position = initial_position
        self.velocity = initial_velocity
        self.acceleration = initial_acceleration
        self.parent_body = parent_body
        self.color = color

    def draw(self):
        """
        Render the celestial body using OpenGL.
        """
        glColor3fv(self.color)
        quad = gluNewQuadric()
        glPushMatrix()
        glTranslatef(*self.position)
        gluSphere(quad, self.radius, 32, 32)
        glPopMatrix()

    def update(self, delta_time: float, masses, positions):
        """
        Update the celestial body's position and velocity.

        Parameters:
        delta_time (float): The time step for the update (s).
        masses (np.array): Array of masses of all other celestial bodies (shape: [n]).
        positions (np.array): Array of position vectors of all other celestial bodies (shape: [n, 3]).
        """
        new_acceleration = calculate_acceleration(self.mass, self.position, masses, positions)
        self.velocity = update_velocity(self.velocity, self.acceleration, new_acceleration, delta_time)
        self.position = update_position(self.position, self.velocity, self.acceleration, delta_time)
        self.acceleration = new_acceleration

    def log(self):
        print(
            f'Name: {self.p_name}, Position: {self.position}, Velocity: {self.velocity}, Acceleration: {self.acceleration}')
