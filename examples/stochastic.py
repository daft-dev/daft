"""
The Quintessential PGM
======================

This is a demonstration of a very common structure found in graphical models.
It has been rendered using Daft's default settings for all the parameters
and it shows off how much beauty is baked in by default.

"""

from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)

import daft

# Instantiate the PGM.
pgm = daft.PGM([5., 3.1], origin=[-0.5, 0.3])

# Hierarchical parameters.
pgm.add_node(daft.Node("alpha", r"$\alpha$", 0.5, 3., fixed=True))
pgm.add_node(daft.Node("weather", r"stochastic", 0.5, 2., aspect=2.5))
pgm.add_node(daft.Node("pop", r"population", 2., 3., aspect=2.5))
pgm.add_node(daft.Node("science", r"target", 2., 2., aspect=2.5))
pgm.add_node(daft.Node("data", r"data set", 1.5, 1., aspect=2.5))
pgm.add_node(daft.Node(r"noise", r"\noindent noise\\ model", 3.7, 1., aspect=2.5))

# Add in the edges.
pgm.add_edge("alpha", "weather")
pgm.add_edge("weather", "data")
pgm.add_edge("pop", "science")
pgm.add_edge("science", "data")
pgm.add_edge("noise", "data")

# And a plate.
pgm.add_plate(daft.Plate([-0.3, 0.5, 3.1, 2.], label=r"data sets",
    shift=-0.1))

# Render and save.
pgm.render()
pgm.figure.savefig("stochastic.pdf")
pgm.figure.savefig("stochastic.png", dpi=150)
