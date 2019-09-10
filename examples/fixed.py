"""
Node Types
==========

There are four default styles of nodes.

"""

import daft

pgm = daft.PGM(aspect=1.5, node_unit=1.75)
pgm.add_node("unobs", r"Unobserved!", 1, 4)
pgm.add_node("obs", r"Observed!", 1, 3, observed=True)
pgm.add_node("alt", r"Alternate!", 1, 2, alternate=True)
pgm.add_node("fixed", r"Fixed!", 1, 1, fixed=True, aspect=1.0, offset=[0, 5])

pgm.render()
pgm.savefig("fixed.pdf")
pgm.savefig("fixed.png", dpi=150)
