"""
Plotting module containing convenicence functions for visualizing cluster chain dynamics.
"""

import matplotlib.pyplot as pl

pl.style.use("fivethirtyeight")
pl.rcParams.update(
    {
        "savefig.edgecolor": "white",
        "savefig.facecolor": "white",
        "figure.edgecolor": "white",
        "figure.facecolor": "white",
        "axes.edgecolor": "white",
        "axes.facecolor": "white",
        "patch.edgecolor": "white",
        "patch.facecolor": "white",
        "patch.force_edgecolor": False,
        "font.size": 12,
    }
)

from .coord_vs_vel_2D import plot_coord_vs_vel_2D

__all__ = ['plot_coord_vs_vel_2D',]