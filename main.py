import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import pygame_gui
from model.celestial_body import CelestialBody

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
    gluPerspective(45, (width / height), 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)

set_perspective(display[0], display[1])

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

# Show the cursor
pygame.mouse.set_visible(True)

# Create Earth and Moon instances
earth = CelestialBody(b_name="Earth", radius=1, color=(0, 0, 1))
moon = CelestialBody(b_name="Moon", radius=0.273, color=(0.5, 0.5, 0.5), orbit_radius=30, orbit_speed=0.1, parent_body=earth)

# Create Mars, Phobos, and Deimos instances
mars = CelestialBody(b_name="Mars", radius=0.532, color=(1, 0, 0), orbit_radius=150, orbit_speed=0.05)
phobos = CelestialBody(b_name="Phobos", radius=0.011, color=(0.5, 0.5, 0.5), orbit_radius=6, orbit_speed=0.2, parent_body=mars)
deimos = CelestialBody(b_name="Deimos", radius=0.006, color=(0.5, 0.5, 0.5), orbit_radius=15, orbit_speed=0.1, parent_body=mars)

# List of celestial bodies
celestial_bodies = [earth, moon, mars, phobos, deimos]

# Initialize Pygame GUI manager
manager = pygame_gui.UIManager(display)

# Create dropdown menu
dropdown_menu = pygame_gui.elements.UIDropDownMenu(
    options_list=[body.name for body in celestial_bodies],
    starting_option='Select Body',
    relative_rect=pygame.Rect((700, 10), (100, 30)),
    manager=manager
)

# Dropdown menu state
dropdown_open = False

# Main loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.VIDEORESIZE:
            display = (event.w, event.h)
            window_surface = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
            set_perspective(display[0], display[1])
            manager.set_window_resolution(display)
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
                dropdown_open = not dropdown_open
        elif event.type == pygame.MOUSEWHEEL:
            zoom_level += event.y  # Adjust zoom level based on wheel movement

        manager.process_events(event)

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

    # Update Pygame GUI
    manager.update(time_delta)

    # Draw Pygame GUI
    manager.draw_ui(window_surface)

    # Update the display
    pygame.display.flip()

pygame.quit()
