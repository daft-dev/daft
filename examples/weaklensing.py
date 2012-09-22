from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)
import daft

if __name__ == "__main__":
    pgm = daft.PGM([4, 3.5], origin=[-0.5, 2])

    pgm.add_node(daft.Node("Omega", r"$\Omega$", 5, 10))
    pgm.add_node(daft.Node("gamma", r"$\gamma$", 3, 10))
    pgm.add_node(daft.Node("obs", r"$\epsilon^\obs_n$", 3, 8, observed=True))
    pgm.add_node(daft.Node("alpha", r"$\alpha$", 7, 8))
    pgm.add_node(daft.Node("true", r"$\epsilon^\true_n$", 5, 8))
    pgm.add_node(daft.Node("sigma", r"$\sigma_n$", 3, 6))
    pgm.add_node(daft.Node("Sigma", r"$\Sigma$", 1, 6))
    pgm.add_node(daft.Node("x", r"$x_n$", 5, 6, observed=True))
    pgm.add_plate(daft.plate([2, 4.5, 4, 4.5], label=r"$n = 1, \ldots, N$"))
    pgm.add_edge("Omega", "gamma")
    pgm.add_edge("gamma", "obs")
    pgm.add_edge("alpha", "true")
    pgm.add_edge("true", "obs")
    pgm.add_edge("x", "obs")
    pgm.add_edge("Sigma", "sigma")
    pgm.add_edge("sigma", "obs")
    pgm.render()
    pgm.figure.savefig("weaklensing.pdf")
    pgm.figure.savefig("weaklensing.png", dpi=200)
