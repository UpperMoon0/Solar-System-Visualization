import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from model.celestial_body import CelestialBody

# Initialize Pygame
pygame.init()
display = (800, 600)
pygame.display.set_caption("Solar System 3D Visualization")
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set the perspective of the OpenGL scene
gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)

# Enable depth testing
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

# Initialize zoom level
zoom_level = -10

# Initialize camera rotation angles
camera_rot_x = 0
camera_rot_y = 0

# Initialize mouse state
mouse_down = False

# Initialize orbit visibility
show_orbit = True

# Create Earth and Moon instances
earth = CelestialBody(radius=1, color=(0, 0, 1))
moon = CelestialBody(radius=0.273, color=(0.5, 0.5, 0.5), orbit_radius=30, orbit_speed=0.1, parent_body=earth)

# Create Mars, Phobos, and Deimos instances
mars = CelestialBody(radius=0.532, color=(1, 0, 0), orbit_radius=150, orbit_speed=0.05)
phobos = CelestialBody(radius=0.011, color=(0.5, 0.5, 0.5), orbit_radius=6, orbit_speed=0.2, parent_body=mars)
deimos = CelestialBody(radius=0.006, color=(0.5, 0.5, 0.5), orbit_radius=15, orbit_speed=0.1, parent_body=mars)

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
    earth.draw()

    # Draw the Moon's orbit path
    if show_orbit:
        moon.draw_orbit()

    # Draw the Moon
    moon.update_position()
    moon.draw()

    # Draw Mars
    mars.update_position()
    mars.draw()

    # Draw Phobos' orbit path
    if show_orbit:
        phobos.draw_orbit()

    # Draw Phobos
    phobos.update_position()
    phobos.draw()

    # Draw Deimos' orbit path
    if show_orbit:
        deimos.draw_orbit()

    # Draw Deimos
    deimos.update_position()
    deimos.draw()

    glPopMatrix()  # End of camera transformations

    # Update the display
    pygame.display.flip()
    pygame.time.wait(10)
