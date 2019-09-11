"""
You can use arbitrarily shitty fonts
====================================

Any fonts that LaTeX or matplotlib supports can be used. Do not take
this example as any kind of implied recommendation unless you plan on
announcing a *huge* discovery!

"""

import daft
from matplotlib import rc

ff = "comic sans ms"
# ff = "impact"
# ff = "times new roman"

rc("font", family=ff, size=12)
rc("text", usetex=False)


pgm = daft.PGM(aspect=2.1, dpi=150)
pgm.add_node("confused", r"confused", 3.0, 3.0)
pgm.add_node("ugly", r"ugly font", 3.0, 2.0, observed=True)
pgm.add_node("bad", r"bad talk", 5.0, 2.0, observed=True)
pgm.add_edge("confused", "ugly")
pgm.add_edge("ugly", "bad")
pgm.add_edge("confused", "bad")

pgm.render()
pgm.savefig("badfont.pdf")
pgm.savefig("badfont.png")
