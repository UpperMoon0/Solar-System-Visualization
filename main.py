import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import math

# Initialize Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set the perspective of the OpenGL scene
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

# Move all objects back so we can see them
glTranslatef(0.0, 0.0, -10)  # Adjusted to zoom out

# Enable depth testing
glEnable(GL_DEPTH_TEST)
# Specify the function used to compare each incoming pixel depth value with the depth value present in the depth buffer
glDepthFunc(GL_LESS)

# Define the properties of the Earth and the Moon
earth_radius = 1
moon_radius = earth_radius * 0.273  # The Moon's radius is 27.3% of the Earth's
earth_color = (0, 0, 1)  # Blue
moon_color = (0.5, 0.5, 0.5)  # Gray
moon_angle = 0  # The Moon's current position in its orbit

# Initialize camera rotation angles
camera_rot_x = 0
camera_rot_y = 0

# Initialize mouse state
mouse_down = False

# Initialize orbit visibility
show_orbit = True


# Function to draw a sphere
def draw_sphere(radius, color):
    glColor3fv(color)
    quad = gluNewQuadric()
    gluSphere(quad, radius, 32, 32)


# Function to draw the orbit path
def draw_orbit():
    glColor3f(1, 1, 1)  # White
    glBegin(GL_LINE_LOOP)
    for i in range(100):
        angle = math.radians(float(i) / 100 * 360.0)
        orbit_x = 3 * math.cos(angle)
        orbit_z = 3 * math.sin(angle)
        glVertex3f(orbit_x, 0, orbit_z)
    glEnd()


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                mouse_down = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_down:
                dx, dy = event.rel
                camera_rot_x += dy * 0.1
                camera_rot_y += dx * 0.1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                show_orbit = not show_orbit

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Apply camera rotation
    glPushMatrix()
    glRotatef(camera_rot_x, 1, 0, 0)
    glRotatef(camera_rot_y, 0, 1, 0)

    # Draw the Earth
    draw_sphere(earth_radius, earth_color)

    # Draw the Moon's orbit path
    if show_orbit:
        draw_orbit()

    # Draw the Moon
    glPushMatrix()
    # Rotate by the Moon's current position in its orbit
    glRotatef(moon_angle, 0, 1, 0)
    # Move to the Moon's position
    glTranslatef(3, 0, 0)
    draw_sphere(moon_radius, moon_color)
    glPopMatrix()

    glPopMatrix()  # End of camera rotation

    # Update the Moon's position
    moon_angle += 0.1

    # Update the display
    pygame.display.flip()
    pygame.time.wait(10)