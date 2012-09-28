#!/usr/bin/env python
"""
One PGM to own them all.
"""

from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)

# Deal with the path for import.
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import daft


if __name__ == "__main__":
    # Instantiate the PGM.
    pgm = daft.PGM([2.3, 2.05], origin=[0.3, 0.3], line_width=2)

    # Hierarchical parameters.
    pgm.add_node(daft.Node("alpha", r"$\alpha$", 0.5, 2, fixed=True))
    pgm.add_node(daft.Node("beta", r"$\beta$", 1.5, 2))

    # Latent variable.
    pgm.add_node(daft.Node("w", r"$w_n$", 1, 1))

    # Data.
    pgm.add_node(daft.Node("x", r"$x_n$", 2, 1, observed=True))

    # Add in the edges.
    pgm.add_edge("alpha", "beta")
    pgm.add_edge("beta", "w")
    pgm.add_edge("w", "x")
    pgm.add_edge("beta", "x")

    # And a plate.
    pgm.add_plate(daft.Plate([0.5, 0.5, 2, 1], label=r"$n = 1, \ldots, N$",
        shift=-0.1))

    # Render and save.
    pgm.render()
    pgm.figure.savefig("classic.pdf")
    pgm.figure.savefig("classic.png", dpi=150)
