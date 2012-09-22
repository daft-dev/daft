from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)
import daft

if __name__ == "__main__":
    pgm = daft.PGM([4, 3.5], origin=[-0.5, 2])
    pgm.add_node(daft.Node("a", r"$a$", 3, 10))
    pgm.add_node(daft.Node("b", r"$b$", 3, 8))
    pgm.add_node(daft.Node("c", r"$c_n$", 3, 6, observed=True))
    pgm.add_plate(daft.Plate([2, 4.5, 4, 2.5], label=r"data $n$"))
    pgm.add_edge("a", "b")
    pgm.add_edge("b", "c")
    pgm.render()
    pgm.figure.savefig("abc.pdf")
    pgm.figure.savefig("abc.png", dpi=200)
