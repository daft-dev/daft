---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

Nodes can go free
=================

You don't need to put ellipses or circles around your node contents,
if you don't want to.

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

pgm = daft.PGM(node_ec="none")
pgm.add_node("cloudy", r"cloudy", 3, 3)
pgm.add_node("rain", r"rain", 2, 2)
pgm.add_node("sprinkler", r"sprinkler", 4, 2)
pgm.add_node("wet", r"grass wet", 3, 1)
pgm.add_edge("cloudy", "rain")
pgm.add_edge("cloudy", "sprinkler")
pgm.add_edge("rain", "wet")
pgm.add_edge("sprinkler", "wet")

pgm.render()
```
