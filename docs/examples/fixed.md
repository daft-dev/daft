---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

Node Types
==========

There are four default styles of nodes.

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

pgm = daft.PGM(aspect=1.5, node_unit=1.75)
pgm.add_node("unobs", r"Unobserved!", 1, 4)
pgm.add_node("obs", r"Observed!", 1, 3, observed=True)
pgm.add_node("alt", r"Alternate!", 1, 2, alternate=True)
pgm.add_node("fixed", r"Fixed!", 1, 1, fixed=True, aspect=1.0, offset=[0, 5])

pgm.render()
```
