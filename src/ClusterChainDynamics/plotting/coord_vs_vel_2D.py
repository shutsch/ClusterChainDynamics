import matplotlib.pyplot as plt
import numpy as np


def plot_coord_vs_vel_2D(positions, velocities, index, path, title="", xlabel=None, ylabel=None):
    """
    Plots a 2D scatter plot of a specified coordinate vs. a specified velocity component.

    Args:
        positions (np.ndarray): Array of shape (N, 3) containing positions of objects.
        velocities (np.ndarray): Array of shape (N, 3) containing velocities of objects.
        index (int): Index of the component to plot (0 for x, 1 for y, 2 for z).
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
    """
    
    label_map = {0: 'x', 1: 'y', 2: 'z'}
    coord_index = label_map.get(index, f'coord{index}')
    
    plt.figure(figsize=(8, 6))
    plt.scatter(positions[:, index], velocities[:, index], alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel if xlabel else f"Position {coord_index}")
    plt.ylabel(ylabel if ylabel else f"Velocity {coord_index}")
    plt.grid(True)
    plt.savefig(path + f"coord{index}_vs_vel{index}.png")
    plt.close()