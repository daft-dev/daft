"""
You can use arbitrary fonts
===========================

Any fonts that LaTeX or matplotlib supports can be used.  Do not take
this example as any kind of implied recommendaton!

"""

from matplotlib import rc
rc("font", family="comic sans ms", size=12)

import daft

pgm = daft.PGM([3.6, 1.8], origin=[2.2, 1.6], directed=False)
asp = 2.1
pgm.add_node(daft.Node("confused", r"confused", 3., 3., aspect=asp))
pgm.add_node(daft.Node("ugly", r"ugly font", 3., 2., aspect=asp))
pgm.add_node(daft.Node("bad", r"bad talk", 5., 2., aspect=asp))
pgm.add_edge("confused", "ugly")
pgm.add_edge("ugly", "bad")
pgm.add_edge("confused", "bad")
pgm.render()
pgm.figure.savefig("badfont.pdf")
pgm.figure.savefig("badfont.png", dpi=150)
