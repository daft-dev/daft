"""
The GALEX Photon Catalog
========================

This is the Hogg & Schiminovich model for how photons turn into
counts in the GALEX satellite data stream.  Note the use of relative
positioning.

"""

import daft
from matplotlib import rc

rc("font", family="serif", size=12)
rc("text", usetex=True)


pgm = daft.PGM()
wide = 1.5
verywide = 1.5 * wide
dy = 0.75

# electrons
el_x, el_y = 2.0, 2.0
pgm.add_plate([el_x - 0.6, el_y - 0.6, 2.2, 2 * dy + 0.3], label="electrons $i$")
pgm.add_node(
    "xabc",
    r"xa$_i$,xabc$_i$,ya$_i$,\textit{etc}",
    el_x + 0.5,
    el_y + 0 * dy,
    aspect=2.3 * wide,
    observed=True,
)
pgm.add_node("xyti", r"$x_i,y_i,t_i$", el_x + 1.0, el_y + 1 * dy, aspect=wide)
pgm.add_edge("xyti", "xabc")

# intensity fields
ph_x, ph_y = el_x + 2.5, el_y + 3 * dy
pgm.add_node("Ixyt", r"$I_{\nu}(x,y,t)$", ph_x, ph_y, aspect=verywide)
pgm.add_edge("Ixyt", "xyti")
pgm.add_node("Ixnt", r"$I_{\nu}(\xi,\eta,t)$", ph_x, ph_y + 1 * dy, aspect=verywide)
pgm.add_edge("Ixnt", "Ixyt")
pgm.add_node("Iadt", r"$I_{\nu}(\alpha,\delta,t)$", ph_x, ph_y + 2 * dy, aspect=verywide)
pgm.add_edge("Iadt", "Ixnt")

# s/c
sc_x, sc_y = ph_x + 1.5, ph_y - 1.5 * dy
pgm.add_node("dark", r"dark", sc_x, sc_y - 1 * dy, aspect=wide)
pgm.add_edge("dark", "xyti")
pgm.add_node("flat", r"flat", sc_x, sc_y, aspect=wide)
pgm.add_edge("flat", "xyti")
pgm.add_node("att", r"att", sc_x, sc_y + 3 * dy)
pgm.add_edge("att", "Ixnt")
pgm.add_node("optics", r"optics", sc_x, sc_y + 2 * dy, aspect=wide)
pgm.add_edge("optics", "Ixyt")
pgm.add_node("psf", r"psf", sc_x, sc_y + 1 * dy)
pgm.add_edge("psf", "xyti")
pgm.add_node("fee", r"f.e.e.", sc_x, sc_y - 2 * dy, aspect=wide)
pgm.add_edge("fee", "xabc")

# sky
pgm.add_node("sky", r"sky", sc_x, sc_y + 4 * dy)
pgm.add_edge("sky", "Iadt")

# stars
star_x, star_y = el_x, el_y + 4 * dy
pgm.add_plate([star_x - 0.6, star_y - 0.6, 2.2, 2 * dy + 0.3], label="stars $n$")
pgm.add_node(
    "star adt", r"$I_{\nu,n}(\alpha,\delta,t)$", star_x + 0.5, star_y + 1 * dy, aspect=verywide
)
pgm.add_edge("star adt", "Iadt")
pgm.add_node("star L", r"$L_{\nu,n}(t)$", star_x + 1, star_y, aspect=wide)
pgm.add_edge("star L", "star adt")
pgm.add_node("star pos", r"$\vec{x_n}$", star_x, star_y)
pgm.add_edge("star pos", "star adt")

# done
pgm.render()
pgm.savefig("galex.pdf")
pgm.savefig("galex.png", dpi=150)
