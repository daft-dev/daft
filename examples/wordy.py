from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)
import daft

if __name__ == "__main__":
    pgm = daft.PGM([4, 3], origin = [1.0, 0.5])
    pgm.add_node(daft.Node("cloudy", r"cloudy", 3, 3, aspect=2.))
    pgm.add_node(daft.Node("rain", r"rain", 2, 2, aspect=2.))
    pgm.add_node(daft.Node("sprinkler", r"sprinkler", 4, 2, aspect=2))
    pgm.add_node(daft.Node("wet", r"grass wet", 3, 1, aspect=2, observed=True))
    pgm.add_edge("cloudy", "rain")
    pgm.add_edge("cloudy", "sprinkler")
    pgm.add_edge("rain", "wet")
    pgm.add_edge("sprinkler", "wet")
    pgm.render()
    pgm.figure.savefig("wordy.pdf")
    pgm.figure.savefig("wordy.png", dpi=200)
