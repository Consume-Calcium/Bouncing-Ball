import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

circle1 = Circle((0, 0), 1, fill=False)

# Parameters
timestep = 0.0001   # Time step
g = -10             # Acceleration
e = 1               # Elasticity
x = [0.01]          # Initial x
y = [1.1]           # Initial y
xdot = [0]          # Initial xdot
ydot = [0]          # Initial ydot

bounces = 0

# Simulate trajectory
while y[-1] > -1:
    # Check collision with the circle
    if (x[-1]**2 + y[-1]**2) <= 1:
        # Calculate polar coordinate position and velocity
        r = np.sqrt(x[-1]**2 + y[-1]**2)
        theta = np.arctan2(y[-1], x[-1])
        rdot = (x[-1] * xdot[-1] + y[-1] * ydot[-1]) / r
        thetadot = (x[-1] * ydot[-1] - y[-1] * xdot[-1]) / r**2

        # Update velocity after collision
        xdot[-1] = -e * rdot * np.cos(theta) - r * thetadot * np.sin(theta)
        ydot[-1] = -e * rdot * np.sin(theta) + r * thetadot * np.cos(theta)

        bounces += 1

    # Update position and velocity
    x.append(x[-1] + xdot[-1] * timestep)
    y.append(y[-1] + ydot[-1] * timestep)
    xdot.append(xdot[-1])
    ydot.append(ydot[-1] + g * timestep)

print("initial [x, y] =", [x[0], y[0]], "bounces:", bounces)
fig, ax = plt.subplots()
plt.plot(x, y, 'k-')
ax.add_patch(circle1)
plt.show()