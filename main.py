import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import math

# Initialize Pygame
pygame.init()
display = (800, 600)
pygame.display.set_caption("Solar System 3D Visualization")
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set the perspective of the OpenGL scene
gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)

# Initialize zoom level
zoom_level = -10

# Enable depth testing
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

# Define the properties of the Earth and the Moon
earth_radius = 1
moon_radius = earth_radius * 0.273
earth_color = (0, 0, 1)
moon_color = (0.5, 0.5, 0.5)
moon_angle = 0

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
    glColor3f(1, 1, 1)
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
            if event.button == 1:
                mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_down:
                dx, dy = event.rel
                camera_rot_x += dy * 0.1
                camera_rot_y += dx * 0.1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                show_orbit = not show_orbit
        elif event.type == pygame.MOUSEWHEEL:
            zoom_level += event.y  # Adjust zoom level based on wheel movement

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Apply camera transformations
    glPushMatrix()
    glTranslatef(0.0, 0.0, zoom_level)
    glRotatef(camera_rot_x, 1, 0, 0)
    glRotatef(camera_rot_y, 0, 1, 0)

    # Draw the Earth
    draw_sphere(earth_radius, earth_color)

    # Draw the Moon's orbit path
    if show_orbit:
        draw_orbit()

    # Draw the Moon
    glPushMatrix()
    glRotatef(moon_angle, 0, 1, 0)
    glTranslatef(3, 0, 0)
    draw_sphere(moon_radius, moon_color)
    glPopMatrix()

    glPopMatrix()  # End of camera transformations

    # Update the Moon's position
    moon_angle += 0.1

    # Update the display
    pygame.display.flip()
    pygame.time.wait(10)
