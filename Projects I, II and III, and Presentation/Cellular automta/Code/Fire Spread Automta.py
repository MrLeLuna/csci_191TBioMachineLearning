import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors


def iterate(forest):
    # create a new empty forest that will be actually be burned instead of our
    # original forrest for convenience
    X1 = np.zeros((ny, nx))
    
    # double for loop to iterate through every cell in the forest expect those on the border
    for indexX in range(1, nx-1):
        for indexY in range(1, ny-1):
            # if the previous forest iteration had a tree at this location
            # then  the current iteration should also have a tree
            # this also help remove trees that were burning in the previous time step
            if forest[indexY, indexX] == TREE:
                X1[indexY, indexX] = TREE
                # check for trees around or current tree to see if they are burning or not
                for dx, dy in neighbourhood:
                    # If a burning tree is diagonal to the current tree  it will have a
                    # reduced probability for the fire to spread
                    if abs(dx) == abs(dy) and np.random.random() < .7:
                        continue
                    # else if a tree is directly adjacent like in von nonhuman model
                    # there still will not be a guarantee for the fire to spread but
                    # rather a high possibility for it spread
                    if forest[indexY + dy, indexX + dx] == FIRE and np.random.random() < .5:
                        X1[indexY, indexX] = FIRE
                        break
            # else there is a random probability for lighting strike to start a fire
            else:
                if np.random.random() <= lightning_strike_prob:
                    X1[indexY, indexX] = FIRE
    # returns the new state of the forrest
    return X1


def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)


# they 3 types of cells we have and there corresponding values
EMPTY, TREE, FIRE = 0, 1, 2
# define the neighborhood model we want to use for our fire simulation here
neighbourhood = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
# setting up the colors information and how we want to use it
colors_list = [(0.1, 0, 0), (0, 0.5, 0.2), (1, 0, 0), 'red']
color_map = colors.ListedColormap(colors_list)
bounds = [0, 1, 2, 3]
norm = colors.BoundaryNorm(bounds, color_map.N)

# What percent of the forest is covered by tree
# you can manually change this value to effect the
# density of the forrest
forest_fraction = 0.8
# the size of the forrest in terms of the x and y dimensions
nx, ny = 100, 100
# Probability of new and of lightning strike to cause a cell to burn.
lightning_strike_prob = 0.0001
# Initialize the forest grid to be a grid of empty tiles
X = np.zeros((ny, nx))
# then randomly generate the forrest using our probabilities to either be a tree or remain empty
X[1:ny-1, 1:nx-1] = np.random.randint(0, 2, size=(ny-2, nx-2))
X[1:ny-1, 1:nx-1] = np.random.random(size=(ny-2, nx-2)) < forest_fraction

# set up out figure for output
fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=color_map, norm=norm)
    
# pass in our initial forrest into the animate function so that
# it can iterate over time to simulate the fire spreading
animate.X = X

# interval decides how often a time step occurs
# I have it set to occur every 16 ms, so we have 60
# updates per second
interval = 16
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=60)
plt.show()
