---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

An undirected graph
===================

This makes the simple point that you don't have to have directions on
your edges; you can have *undirected* graphs.  (Also, the nodes don't
need to have labels!)

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
import itertools

# Instantiate the PGM.
pgm = daft.PGM(node_unit=0.4, grid_unit=1, directed=False)

for i, (xi, yi) in enumerate(itertools.product(range(1, 5), range(1, 5))):
    pgm.add_node(str(i), "", xi, yi)

for e in [
    (4, 9),
    (6, 7),
    (3, 7),
    (10, 11),
    (10, 9),
    (10, 14),
    (10, 6),
    (10, 7),
    (1, 2),
    (1, 5),
    (1, 0),
    (1, 6),
    (8, 12),
    (12, 13),
    (13, 14),
    (15, 11),
]:
    pgm.add_edge(str(e[0]), str(e[1]))

# Render and save.
pgm.render()
```
