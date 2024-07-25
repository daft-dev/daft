import daft
import matplotlib as mpl
import matplotlib.pyplot as plt

# Colors.
no_circle = {"ec": "#fff"}
pgm = daft.PGM(grid_unit=1.5, node_unit=1, dpi=200)

# x_offset, y_offset = -0.5, 0.5  # adjust the coordinates of the nodes
x_offset, y_offset = 0, 0
pgm.add_node("z1", r"$z_1$", 1 + x_offset, 1 + y_offset)
pgm.add_node("z2", r"$z_2$", 2 + x_offset, 1 + y_offset)
pgm.add_node("z...", r"$\cdots$", 3 + x_offset, 1 + y_offset, plot_params=no_circle)
pgm.add_node("zT", r"$z_T$", 4 + x_offset, 1 + y_offset)
pgm.add_node("y1", r"$x_1$", 1 + x_offset, 2.3 + y_offset)
pgm.add_node("y2", r"$x_2$", 2 + x_offset, 2.3 + y_offset)
pgm.add_node("y...", r"$\cdots$", 3 + x_offset, 2.3 + y_offset, plot_params=no_circle)
pgm.add_node("yT", r"$x_T$", 4 + x_offset, 2.3 + y_offset)
pgm.add_node("x1", r"$x_1$", 1 + x_offset, y_offset)
pgm.add_node("x2", r"$x_2$", 2 + x_offset, y_offset)
pgm.add_node("x...", r"$\cdots$", 3 + x_offset, y_offset, plot_params=no_circle)
pgm.add_node("xT", r"$x_T$", 4 + x_offset, y_offset)

# Edges.
# pgm.add_edge("z1", "z2")
# pgm.add_edge("z2", "z...")
# pgm.add_edge("z...", "zT")
pgm.add_edge("x1", "z1")
pgm.add_edge("x2", "z2")
pgm.add_edge("xT", "zT")
pgm.add_edge("z1", "y2")
pgm.add_edge("z1", "yT")
pgm.add_edge("z2", "yT")

# Render and save.
# pgm.render()
# plt.tight_layout()
# plt.show()
pgm.show()
# pgm.figure.savefig("../src/nar.png")
