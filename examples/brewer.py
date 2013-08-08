"""
Brewer's project, sort of
=========================

This uses a HACK of `Plate` to put a label on the plot.
"""

from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)

import daft

pgm = daft.PGM([5., 2.5], origin=[2.0, 0.0], aspect=2.1)
pgm.add_node(daft.Node("counts", r"$dN/dm$", 6.0, 2.0))
pgm.add_node(daft.Node("stars", r"stars", 4.5, 2.0,))
pgm.add_node(daft.Node("pixels", r"pixels", 3.0, 2.0, observed=True))
pgm.add_node(daft.Node("psf", r"psf", 4.5, 1.0))
pgm.add_node(daft.Node("noise", r"noise", 3.0, 1.0))
pgm.add_edge("stars", "pixels")
pgm.add_edge("psf", "pixels")
pgm.add_edge("noise", "pixels")
pgm.add_edge("counts", "stars")
pgm.add_plate(daft.Plate([2.0, 0.0, 7.0, 2.5],
                         label=r"$p(\mbox{pixels}\,|\,\mbox{stars})\,p(\mbox{stars}\,|\,dN/dm)\,p(dN/dm)$",
                         label_offset=[30,10],
                         rect_params={"ec": "none",}))
pgm.render()
pgm.figure.savefig("brewer.pdf")
pgm.figure.savefig("brewer.png", dpi=300)
