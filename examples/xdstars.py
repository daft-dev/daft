"""
Extreme deconvolution of stars
==============================

The (very simple) model that transformed SDSS-III.

"""

from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)

import daft

# Instantiate the PGM.
pgm = daft.PGM([2.3, 2.05], origin=[0.3, 0.3])

# Hierarchical parameters.
pgm.add_node(daft.Node("theta", r"$\theta$", 0.5, 2, fixed=True))
pgm.add_node(daft.Node("sigma", r"$\Sigma$", 1.5, 2))

# Latent variable.
pgm.add_node(daft.Node("X", r"$X_n$", 1, 1))

# Data.
pgm.add_node(daft.Node("x", r"$x_n$", 2, 1, observed=True))

# Add in the edges.
pgm.add_edge("theta", "X")
pgm.add_edge("sigma", "x")
pgm.add_edge("X", "x")

# And a plate.
pgm.add_plate(daft.Plate([0.5, 0.5, 2, 1], label=r"stars $n$", shift=-0.1))

# Render and save.
pgm.render()
pgm.figure.savefig("xdstars.pdf")
pgm.figure.savefig("xdstars.png", dpi=150)
