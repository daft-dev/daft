"""
Hayabusa
========

No comment.

"""

from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)
import daft

pgm = daft.PGM([4.8, 3.2], origin=[-0.4, -0.7])

# Hierarchical parameters.
pgm.add_node(daft.Node("theta", r"$\theta$", 0, 1))
pgm.add_node(daft.Node("Omega", r"$\Omega$", 4, 1))
pgm.add_node(daft.Node("Sigma", r"$\Sigma$", 0, 0))

# spectral measurements
pgm.add_node(daft.Node("a", r"$a_n$", 1, 2, observed=True))
pgm.add_node(daft.Node("z", r"$z_n$", 2, 2, observed=True))

# Latent variables.
pgm.add_node(daft.Node("M", r"$M_n$", 1, 1))
pgm.add_edge("a", "M")
pgm.add_edge("theta", "M")
pgm.add_node(daft.Node("K", r"$K_n$", 2, 1))
pgm.add_edge("z", "K")
pgm.add_node(daft.Node("DM", r"$DM_n$", 3, 1))
pgm.add_edge("z", "DM")
pgm.add_edge("Omega", "DM")

# Data.
pgm.add_node(daft.Node("m", r"$m_n$", 2, 0, observed=True))
pgm.add_edge("M", "m")
pgm.add_edge("K", "m")
pgm.add_edge("DM", "m")
pgm.add_edge("Sigma", "m")

# And a plate.
pgm.add_plate(daft.Plate([0.5, -0.6, 3, 3], label=r"quasars $n$"))

# Render and save.
pgm.render()
pgm.figure.savefig("hayabusa.pdf")
pgm.figure.savefig("hayabusa.png", dpi=150)
