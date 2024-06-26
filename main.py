import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

from gui.gui_manager import GuiManager
from entity.celestial_body import CelestialBody

# Initialize Pygame
pygame.init()
display = (800, 600)
window_surface = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
pygame.display.set_caption("Solar System 3D Visualization")


# Set the perspective of the OpenGL scene
def set_perspective(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / height), 0.1, 1000000)
    glMatrixMode(GL_MODELVIEW)


set_perspective(display[0], display[1])

# Enable depth testing
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

# Initialize zoom level
zoom_level = -20

# Initialize camera rotation angles
camera_rot_x = 0
camera_rot_y = 0

# Initialize mouse state
mouse_down = False

# Initialize orbit visibility
show_orbit = True

# Show the cursor
pygame.mouse.set_visible(True)

au = 23455.62  # Astronomical unit in earth radii

sun = CelestialBody(p_name="Sun",
                    radius=4,
                    mass=10000,
                    color=(1, 1, 0))

# Create Mercury, Venus, Earth, and Moon instances
# mercury = CelestialBody(b_name="Mercury", radius=0.35, color=(0.5, 0.5, 0.5), orbit_radius=10, orbit_speed=0.1, parent_body=sun)
# venus = CelestialBody(b_name="Venus", radius=1, color=(1, 0.5, 0), orbit_radius=15, orbit_speed=0.08, parent_body=sun)
earth = CelestialBody(p_name="Earth",
                      radius=1,
                      mass=10,
                      color=(0, 0, 1),
                      initial_position=np.array([20, 0, 0]),
                      initial_velocity=np.array([0, 0, -4.16e-05]),
                      parent_body=sun)
# moon = CelestialBody(b_name="Moon", radius=0.273, color=(0.5, 0.5, 0.5), orbit_radius=3, orbit_speed=0.1, parent_body=earth)

# Create Mars, Phobos, and Deimos instances
# mars = CelestialBody(b_name="Mars", radius=0.532, color=(1, 0, 0), orbit_radius=35, orbit_speed=0.05, parent_body=sun)
# phobos = CelestialBody(b_name="Phobos", radius=0.2, color=(0.5, 0.5, 0.5), orbit_radius=4, orbit_speed=0.2, parent_body=mars)
# deimos = CelestialBody(b_name="Deimos", radius=0.15, color=(0.5, 0.5, 0.5), orbit_radius=6, orbit_speed=0.1, parent_body=mars)

# List of celestial bodies
celestial_bodies = [
    sun, earth
]

# Create GuiManager instance
gui_manager = GuiManager(celestial_bodies, display)

# Main loop
clock = pygame.time.Clock()
is_running = True
last_orbit_prediction_update = pygame.time.get_ticks()
speed_up = 100

while is_running:
    time_delta = 1 * speed_up
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.VIDEORESIZE:
            display = (event.w, event.h)
            window_surface = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
            set_perspective(display[0], display[1])
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
            elif event.key == pygame.K_p:
                gui_manager.dropdown_menu.open = not gui_manager.dropdown_menu.open
        elif event.type == pygame.MOUSEWHEEL:
            zoom_level += event.y

        gui_manager.dropdown_menu.handle_event(event)

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Apply camera transformations
    glPushMatrix()
    glTranslatef(0.0, 0.0, zoom_level)
    glRotatef(camera_rot_x, 1, 0, 0)
    glRotatef(camera_rot_y, 0, 1, 0)
    if gui_manager.target_body:
        glTranslatef(*[-x for x in gui_manager.target_body.position])

    # Draw the celestial bodies
    for body in celestial_bodies:
        other_bodies = [b for b in celestial_bodies if b != body]
        other_masses = np.array([b.mass for b in other_bodies])
        other_positions = np.array([b.position for b in other_bodies])
        body.update(time_delta, other_masses, other_positions)
        if show_orbit:
            current_time = pygame.time.get_ticks()
            if current_time > last_orbit_prediction_update + 50:
                body.predict_orbit(future_time=100000 * speed_up,
                                   time_step=time_delta * 100,
                                   masses=other_masses,
                                   positions=other_positions)
                last_orbit_prediction_update = current_time
            body.draw_predicted_orbit()
        body.draw()
        body.log()

    glPopMatrix()  # End of camera transformations

    # Draw the dropdown menu if open
    gui_manager.draw()

    # Update the display
    pygame.display.flip()

pygame.quit()
