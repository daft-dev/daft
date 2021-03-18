import daft

with daft.PGM() as pgm:
    pgm.add_node(
        daft.Node(
            "d",
            "D",
            0,
            0,
            plot_params=dict(fc="white"),
            fontsize=17,
            offset=(0, -1),
            label_params=dict(fontweight="bold"),
        )
    )
    pgm.render()
    pgm.figure.patch.set_facecolor("none")
    pgm.ax.patch.set_facecolor("none")
    pgm.figure.savefig("favicon.png", transparent=True)
