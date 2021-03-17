---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

You can use arbitrarily bad fonts
=================================

Any fonts that LaTeX or matplotlib supports can be used. Do not take
this example as any kind of implied recommendation unless you plan on
announcing a *huge* discovery!

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
import matplotlib.pyplot as plt

# ff = "comic sans ms"
# ff = "impact"
ff = "times new roman"
plt.rcParams["font.family"] = ff

pgm = daft.PGM(aspect=2.1, dpi=150)
pgm.add_node("confused", r"confused", 3.0, 3.0)
pgm.add_node("ugly", r"ugly font", 3.0, 2.0, observed=True)
pgm.add_node("bad", r"bad talk", 5.0, 2.0, observed=True)
pgm.add_edge("confused", "ugly")
pgm.add_edge("ugly", "bad")
pgm.add_edge("confused", "bad")

pgm.render()
```
