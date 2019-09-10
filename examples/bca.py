import daft
from matplotlib import rc

rc("font", family="serif", size=12)
rc("text", usetex=True)


pgm = daft.PGM()
pgm.add_node("a", r"$a$", 1, 5)
pgm.add_node("b", r"$b$", 1, 4)
pgm.add_node("c", r"$c_n$", 1, 3, observed=True)
pgm.add_plate([0.5, 2.25, 1, 1.25], label=r"data $n$")
pgm.add_edge("a", "b")
pgm.add_edge("b", "c")

pgm.render()
pgm.savefig("bca.pdf")
pgm.savefig("bca.png", dpi=150)
