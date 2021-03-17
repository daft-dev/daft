---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

Nodes can contain words
=======================

We here at **Daft** headquarters tend to put symbols (variable
names) in our graph nodes.  But you don't have to if you don't
want to.

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

pgm = daft.PGM()
pgm.add_node("cloudy", r"cloudy", 3, 3, aspect=1.8)
pgm.add_node("rain", r"rain", 2, 2, aspect=1.2)
pgm.add_node("sprinkler", r"sprinkler", 4, 2, aspect=2.1)
pgm.add_node("wet", r"grass wet", 3, 1, aspect=2.4, observed=True)
pgm.add_edge("cloudy", "rain", label=r"65\%", xoffset=-0.1, label_params={"rotation": 45})
pgm.add_edge("cloudy", "sprinkler", label=r"35\%", xoffset=0.1, label_params={"rotation": -45})
pgm.add_edge("rain", "wet")
pgm.add_edge("sprinkler", "wet")

pgm.render()
```
