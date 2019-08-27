#!/usr/bin/env python
"""
That's an awfully DAFT logo!

"""

from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)

import daft

# Instantiate the PGM.
pgm = daft.PGM((3.7, 0.7), origin=(0.15, 0.15))

pgm.add_node("d", r"$D$", 0.5, 0.5)
pgm.add_node("a", r"$a$", 1.5, 0.5, observed=True)
pgm.add_node("f", r"$f$", 2.5, 0.5)
pgm.add_node("t", r"$t$", 3.5, 0.5)

pgm.add_edge("d", "a")
pgm.add_edge("a", "f")
pgm.add_edge("f", "t")

pgm.render()
pgm.savefig("logo.pdf")
pgm.savefig("logo.png", dpi=200, transparent=True)
