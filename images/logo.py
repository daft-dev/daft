import daft

with daft.PGM() as pgm:
    pgm.add_node(
        daft.Node(
            "d",
            "D",
            0,
            0,
            plot_params=dict(fc="#d8dee9"),
            fontsize=17,
            offset=(0, -2),
            label_params=dict(fontweight="bold", color="#2e3440"),
        )
    )
    pgm.add_node(
        daft.Node(
            "a",
            "A",
            1,
            0,
            plot_params=dict(fc="#4c566a"),
            fontsize=17,
            offset=(0, -2),
            label_params=dict(color="#eceff4"),
        )
    )
    pgm.add_node(
        daft.Node(
            "f",
            "F",
            2,
            0,
            plot_params=dict(fc="#d8dee9"),
            fontsize=17,
            offset=(0, -2),
            label_params=dict(color="#2e3440"),
        )
    )
    pgm.add_node(
        daft.Node(
            "t",
            "T",
            3,
            0,
            plot_params=dict(fc="#d8dee9"),
            fontsize=17,
            offset=(0, -2),
            label_params=dict(color="#2e3440"),
        )
    )
    pgm.add_edge("d", "a")
    pgm.add_edge("a", "f")
    pgm.add_edge("f", "t")
    pgm.render()
    pgm.figure.savefig("logo.png", transparent=True, dpi=250)
