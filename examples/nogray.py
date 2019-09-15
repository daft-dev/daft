"""
Alternative Observed Node Styles
================================

.. module:: daft

This model is the same as `the classic </examples/classic>`_ model but the
"observed" :class:`Node` is indicated by a double outline instead of shading.
This particular example uses the ``inner`` style but ``outer`` is also an
option for a different look.

"""

import daft
from matplotlib import rc

rc("font", family="serif", size=12)
rc("text", usetex=True)


pgm = daft.PGM(observed_style="inner")

# Hierarchical parameters.
pgm.add_node("alpha", r"$\alpha$", 0.5, 2, fixed=True)
pgm.add_node("beta", r"$\beta$", 1.5, 2)

# Latent variable.
pgm.add_node("w", r"$w_n$", 1, 1)

# Data.
pgm.add_node("x", r"$x_n$", 2, 1, observed=True)

# Add in the edges.
pgm.add_edge("alpha", "beta")
pgm.add_edge("beta", "w")
pgm.add_edge("w", "x")
pgm.add_edge("beta", "x")

# And a plate.
pgm.add_plate([0.5, 0.5, 2, 1], label=r"$n = 1, \ldots, N$", shift=-0.1)

# Render and save.
pgm.render()
pgm.savefig("nogray.pdf")
pgm.savefig("nogray.png", dpi=150)
