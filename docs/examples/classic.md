---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

The Quintessential PGM
======================

This is a demonstration of a very common structure found in graphical models.
It has been rendered using Daft's default settings for all the parameters
and it shows off how much beauty is baked in by default.

```{code-cell}
:tags: [remove-cell]
import matplotlib.pyplot as mpl
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.size"] = 12
mpl.rcParams["text.usetex"] = True
mpl.rcParams["figure.dpi"] = 150
```

```{code-cell}
import daft

# Instantiate the PGM.
pgm = daft.PGM()

# Hierarchical parameters.
pgm.add_node("alpha", r"$\alpha$", 0.5, 2, fixed=True)
pgm.add_node("beta", r"$\beta$", 1.5, 2)

# Latent variable.
pgm.add_node("w", r"$w_n$", 1, 1)

# Data.
pgm.add_node("x", r"$x_n$", 2, 1, observed=True)

# Add in the edges.
pgm.add_edge("alpha", "beta")
pgm.add_edge("beta", "w")
pgm.add_edge("w", "x")
pgm.add_edge("beta", "x")

# And a plate.
pgm.add_plate([0.5, 0.5, 2, 1], label=r"$n = 1, \cdots, N$", shift=-0.1)

# Render and save.
pgm.render()
```
