#!/usr/bin/env python
"""
That's an awfully DAFT logo!

"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import daft


if __name__ == "__main__":
    # Instantiate the PGM.
    pgm = daft.PGM((4, 1))

    pgm.add_node(daft.Node("d", r"$D$", 0.5, 0.5))
    pgm.add_node(daft.Node("a", r"$a$", 1.5, 0.5, observed=True))
    pgm.add_node(daft.Node("f", r"$f$", 2.5, 0.5))
    pgm.add_node(daft.Node("t", r"$t$", 3.5, 0.5))

    pgm.add_edge("d", "a")
    pgm.add_edge("a", "f")
    pgm.add_edge("f", "t")

    pgm.render()
    pgm.figure.savefig("logo.png", dpi=200)
