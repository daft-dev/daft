from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)

import daft

pgm = daft.PGM()
pgm.add_node("omega", r"$\omega$", 2, 5)
pgm.add_node("true", r"$\tilde{X}_n$", 2, 4)
pgm.add_node("obs", r"$X_n$", 2, 3, observed=True)
pgm.add_node("alpha", r"$\alpha$", 3, 4)
pgm.add_node("Sigma", r"$\Sigma$", 0, 3)
pgm.add_node("sigma", r"$\sigma_n$", 1, 3)
pgm.add_plate([0.5, 2.25, 2, 2.25], label=r"stars $n$")
pgm.add_edge("omega", "true")
pgm.add_edge("true", "obs")
pgm.add_edge("alpha", "true")
pgm.add_edge("Sigma", "sigma")
pgm.add_edge("sigma", "obs")

pgm.render()
pgm.savefig("gaia.pdf")
pgm.savefig("gaia.png", dpi=150)
