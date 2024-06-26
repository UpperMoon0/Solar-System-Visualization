import numpy as np

# Gravitational constant
G = 6.67430e-11  # m^3 kg^-1 s^-2
epsilon = 1e-3  # Softening parameter


def unit_vector(r1, r2):
    """
    Calculate the unit vector from r1 to r2.

    Parameters:
    r1 (np.array): Position vector of the first object (shape: [3]).
    r2 (np.array): Position vector of the second object (shape: [3]).

    Returns:
    np.array: The unit vector from r1 to r2.
    """
    r12 = r2 - r1  # Distance vector from r1 to r2
    distance = np.linalg.norm(r12)  # Magnitude of the distance vector
    if distance == 0:
        raise ValueError("The positions of the two masses are identical; can't compute the unit vector.")
    return r12 / distance


def euclidean_distance(r1, r2):
    """
    Calculate the Euclidean distance between two 3D position vectors.

    Parameters:
    r1 (np.array): Position vector of the first object (shape: [3]).
    r2 (np.array): Position vector of the second object (shape: [3]).

    Returns:
    float: The Euclidean distance between the two position vectors.
    """
    r12_vector = r2 - r1  # Distance vector
    distance = np.linalg.norm(r12_vector)  # Euclidean distance
    return distance


def gravitational_force(m1, m2, r1, r2):
    """
    Calculate the gravitational force between two masses.

    Parameters:
    m1 (float): Mass of the first object (kg).
    m2 (float): Mass of the second object (kg).
    r1 (np.array): Position vector of the first object (shape: [3]).
    r2 (np.array): Position vector of the second object (shape: [3]).

    Returns:
    np.array: Gravitational force vector acting on m1 due to m2.
    """
    distance = euclidean_distance(r1, r2)
    if distance == 0:
        raise ValueError("The positions of the two masses are identical; can't compute the gravitational force.")

    unit_vec = unit_vector(r1, r2)
    force_magnitude = G * m1 * m2 / (distance ** 2 + epsilon ** 2) ** (3 / 2)
    force_vector = force_magnitude * unit_vec

    return force_vector


def calculate_acceleration(m1, r1, masses, positions):
    """
    Calculate the acceleration of a mass due to gravitational forces from multiple masses.

    Parameters:
    m1 (float): Mass of the object being accelerated (kg).
    r1 (np.array): Position vector of the object being accelerated (shape: [3]).
    positions (np.array): Position vectors of all other masses (shape: [n, 3]).
    masses (np.array): Masses of all other objects (shape: [n]).

    Returns:
    np.array: Acceleration vector of the object being accelerated (shape: [3]).
    """
    net_force = np.array([0.0, 0.0, 0.0])  # Initialize net force vector

    for i in range(len(masses)):
        if np.array_equal(r1, positions[i]):
            continue
        force = gravitational_force(m1, masses[i], r1, positions[i])
        net_force += force

    acceleration_vector = net_force / m1

    return acceleration_vector


def update_position(position, velocity, acceleration, delta_time):
    """
    Update the position of an object using Velocity Verlet integration.

    Parameters:
    position (np.array): Current position vector of the object (shape: [3]).
    velocity (np.array): Current velocity vector of the object (shape: [3]).
    acceleration (np.array): Current acceleration vector of the object (shape: [3]).
    delta_time (float): The time step for the update (s).

    Returns:
    np.array: New position vector of the object (shape: [3]).
    """
    return position + velocity * delta_time + 0.5 * acceleration * delta_time ** 2


def update_velocity(velocity, acceleration, new_acceleration, delta_time):
    """
    Update the velocity of an object using Velocity Verlet integration.

    Parameters:
    velocity (np.array): Current velocity vector of the object (shape: [3]).
    acceleration (np.array): Current acceleration vector of the object (shape: [3]).
    new_acceleration (np.array): New acceleration vector of the object (shape: [3]).
    delta_time (float): The time step for the update (s).

    Returns:
    np.array: New velocity vector of the object (shape: [3]).
    """
    return velocity + 0.5 * (acceleration + new_acceleration) * delta_time
