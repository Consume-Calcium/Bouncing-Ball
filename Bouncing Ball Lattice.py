import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Parameters
timestep = 10**(-14)    # Time step in seconds
a = -10**(21)           # Acceleration of electrons due to electric field in bohr radii per second^2
e = 1                   # Elasticity of collisions
num_circles_x = 2       # Number of circles along x-axis
num_circles_y = 10      # Number of circles along y-axis

# Simulate particle motion
def particle_traj(x, y, xdot, ydot, a, e, radius, circles, lattice_width):

    bounces = 0

    while y[-1] > -1:
        # Check for collisions with each circle in the lattice
        for circle in circles:
            circle_center = circle.center
            if ((x[-1] - circle_center[0])**2 + (y[-1] - circle_center[1])**2) <= radius**2:
                # Calculate polar coordinates with respect to the circle the particle collided with
                r = np.sqrt((x[-1] - circle_center[0])**2 + (y[-1] - circle_center[1])**2)
                theta = np.arctan2((y[-1] - circle_center[1]), (x[-1] - circle_center[0]))
                rdot = ((x[-1] - circle_center[0]) * xdot + (y[-1] - circle_center[1]) * ydot) / r
                thetadot = ((x[-1] - circle_center[0]) * ydot - (y[-1] - circle_center[1]) * xdot) / r**2

                # Update velocity after collision
                xdot = -e * rdot * np.cos(theta) - r * thetadot * np.sin(theta)
                ydot = -e * rdot * np.sin(theta) + r * thetadot * np.cos(theta)

                bounces += 1
                # Sometimes the particle gets stuck inside a sphere so this ends the simulation if that happens
                if bounces >= 100000:
                    return None

        # Update position and velocity
        x.append(x[-1] + xdot * timestep)
        y.append(y[-1] + ydot * timestep)
        ydot += a * timestep

        # Periodic boundary conditions
        if x[-1] < -1.5:
            x[-1] += lattice_width + 3
        elif x[-1] > lattice_width + 1.5:
            x[-1] -= lattice_width + 3

    return len(x) * timestep

# Monte-Carlo simulation to estimate electron mobility
def mc(r, s): # r is the ion radius and s is the seperation between ions
    np.random.seed(634)

    radius = r          # Radius of the circles
    spacing_x = s       # Spacing between circles along x-axis
    spacing_y = s       # Spacing between circles along y-axis
    lattice_width = (num_circles_x - 1) * spacing_x
    lattice_height = (num_circles_y - 1) * spacing_y

    # Create lattice of circles
    circles = []
    for i in range(num_circles_x):
        for j in range(num_circles_y):
            circle_center = (i * spacing_x + (1/4 * spacing_x + (-1)**j * 1/4 * spacing_x), j * spacing_y)
            circles.append(Circle(circle_center, radius, fill=False))

    for j in range(num_circles_y):
        circle_center = ((-1.5/2 - 1.5/2 * (-1)**j) + ((lattice_width + spacing_x)/2 - (lattice_width + spacing_x)/2 * (-1)**j), j * spacing_y)
        circles.append(Circle(circle_center, radius, fill=False))

    # Calulate time for electron to reach the bottom of the lattice for random initial x coordinate
    times = []
    for i in range(10):
        x = [np.random.uniform(0, spacing_x)]
        y = [lattice_height + r + 0.1]

        xdot = 0
        ydot = 0

        time = particle_traj(x, y, xdot, ydot, a, e, radius, circles, lattice_width)
        if time is not None:
            times.append(time)

    # Average times
    time_ave = np.average(times)
    time_error = np.sqrt(np.average(np.array(times)**2) - time_ave**2)

    # Average vertical velocity
    vel_ave = (lattice_height + 2 * r + 0.1) / time_ave
    vel_error = (lattice_height + 2 * r + 0.1) / time_ave**2 * time_error

    # Electron mobility
    electron_mobility = vel_ave / abs(a)
    electron_mobility_error = vel_error / abs(a)

    print(f"{electron_mobility} ± {electron_mobility_error}")

# Prints electron mobilities with errors in atomic units 
print('Aluminium')
mc(1.011, 7.652)

print('Copper')
mc(1.379, 6.831)

print('Gold')
mc(1.606, 7.707)

print('Silver')
mc(1.417, 7.721)
