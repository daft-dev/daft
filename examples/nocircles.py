from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)
import daft

if __name__ == "__main__":
    pgm = daft.PGM([2.9, 2.4], origin = [1.7, 0.8])
    pps = {"ec": "none"}
    pgm.add_node(daft.Node("cloudy", r"cloudy", 3, 3, plot_params=pps))
    pgm.add_node(daft.Node("rain", r"rain", 2, 2, plot_params=pps))
    pgm.add_node(daft.Node("sprinkler", r"sprinkler", 4, 2, plot_params=pps))
    pgm.add_node(daft.Node("wet", r"grass wet", 3, 1, plot_params=pps))
    pgm.add_edge("cloudy", "rain")
    pgm.add_edge("cloudy", "sprinkler")
    pgm.add_edge("rain", "wet")
    pgm.add_edge("sprinkler", "wet")
    pgm.render()
    pgm.figure.savefig("nocircles.pdf")
    pgm.figure.savefig("nocircles.png", dpi=150)
