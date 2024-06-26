import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from physics import acceleration, position, velocity


class CelestialBody:
    def __init__(self,
                 p_name,
                 radius,
                 mass,
                 color,
                 initial_position=np.array([0, 0, 0], dtype=np.float32),
                 initial_velocity=np.array([0, 0, 0], dtype=np.float32),
                 initial_acceleration=np.array([0, 0, 0], dtype=np.float32),
                 parent_body=None):
        """
        Initialize a celestial body.

        Parameters:
        p_name (str): Name of the celestial body.
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
        self.position = np.array(initial_position, dtype=np.float32)
        self.velocity = np.array(initial_velocity, dtype=np.float32)
        self.acceleration = np.array(initial_acceleration, dtype=np.float32)
        self.parent_body = parent_body
        self.color = color
        self.initial_position = np.array(initial_position, dtype=np.float32)
        self.initial_velocity = np.array(initial_velocity, dtype=np.float32)
        self.predicted_positions = []

    def draw(self):
        """
        Render the celestial body using OpenGL.
        """
        glColor3fv(self.color)
        quad = gluNewQuadric()
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        gluSphere(quad, self.radius, 32, 32)
        glPopMatrix()

    def update(self, delta_time: float, masses, positions):
        """
        Update the celestial body's position, velocity, and acceleration.

        Parameters:
        delta_time (float): The time step for the update (s).
        masses (np.array): Array of masses of all other celestial bodies (shape: [n]).
        positions (np.array): Array of position vectors of all other celestial bodies (shape: [n, 3]).
        """
        self.acceleration = acceleration(self.mass, self.position, masses, positions)
        self.velocity = velocity(self.velocity, self.acceleration, self.acceleration, delta_time)
        self.position = position(self.position, self.velocity, self.acceleration, delta_time)

    def predict_orbit(self, future_time, time_step, masses, positions):
        future_position = self.position.copy()
        future_velocity = self.velocity.copy()
        future_acceleration = self.acceleration.copy()
        self.predicted_positions = [future_position.copy()]

        for _ in np.arange(0, future_time, time_step):
            future_velocity = velocity(future_velocity, future_acceleration, future_acceleration, time_step)
            future_position = position(future_position, future_velocity, future_acceleration, time_step)
            self.predicted_positions.append(future_position.copy())

    def draw_predicted_orbit(self):
        if self.parent_body is None or len(self.predicted_positions) <= 1:
            return

        # Extract positions into a numpy array for OpenGL
        positions_array = np.array(self.predicted_positions, dtype=np.float32)

        # Enable vertex array
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, positions_array)

        # Draw the line strip
        glColor3fv(self.color)
        glDrawArrays(GL_LINE_STRIP, 0, len(self.predicted_positions))

        # Disable vertex array after drawing
        glDisableClientState(GL_VERTEX_ARRAY)

    def log(self):
        print(
            f'Name: {self.p_name}, Position: {self.position}, Velocity: {self.velocity}, Acceleration: {self.acceleration}')
