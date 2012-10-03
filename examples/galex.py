"""
The GALEX Photon Catalog
========================

This is the Hogg \& Schiminovich model for how photons turn into
counts in the GALEX satellite data stream.  Note the use of relative
positioning.

"""

from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)
import daft
pgm = daft.PGM([5.8, 6.6], origin=[1.2, 1.1])
wide = 1.5
verywide = 1.5 * wide

# electrons
el_x, el_y = 2., 2.
pgm.add_plate(daft.Plate([el_x - 0.5, el_y - 0.6, 2., 2.], label="electrons $i$"))
pgm.add_node(daft.Node("raw6", r"raw6$_i$", el_x, el_y + 1, aspect=wide, observed=True))
pgm.add_node(daft.Node("xabc", r"xa$_i$,xabc$_i$,ya$_i$,\textit{etc}", el_x + 0.5, el_y, aspect=2.3 * wide))
pgm.add_edge("xabc", "raw6")
pgm.add_node(daft.Node("xyti", r"$x_i,y_i,t_i$", el_x + 1., el_y + 1, aspect=wide))
pgm.add_edge("xyti", "xabc")

# intensity fields
ph_x, ph_y = 4.5, 4.
pgm.add_node(daft.Node("Ixyt", r"$I_{\nu}(x,y,t)$", ph_x, ph_y, aspect=verywide))
pgm.add_edge("Ixyt", "xyti")
pgm.add_node(daft.Node("Ixnt", r"$I_{\nu}(\xi,\eta,t)$", ph_x, ph_y + 1, aspect=verywide))
pgm.add_edge("Ixnt", "Ixyt")
pgm.add_node(daft.Node("Iadt", r"$I_{\nu}(\alpha,\delta,t)$", ph_x, ph_y + 2, aspect=verywide))
pgm.add_edge("Iadt", "Ixnt")

# s/c
pgm.add_node(daft.Node("fee", r"fee", el_x + 2, el_y))
pgm.add_edge("fee", "xyti")
pgm.add_edge("fee", "xabc")
pgm.add_node(daft.Node("dark", r"dark", el_x + 3, el_y, aspect=wide))
pgm.add_edge("dark", "xyti")
pgm.add_node(daft.Node("flat", r"flat", el_x + 3, el_y + 1, aspect=wide))
pgm.add_edge("flat", "xyti")
pgm.add_node(daft.Node("att", r"att", ph_x + 1.5, ph_y + 1))
pgm.add_edge("att", "Ixnt")
pgm.add_node(daft.Node("optics", r"optics", ph_x + 1.5, ph_y, aspect=wide))
pgm.add_edge("optics", "Ixyt")
pgm.add_node(daft.Node("psf", r"psf", ph_x + 1.5, ph_y - 1))
pgm.add_edge("psf", "Ixyt")

# sky
pgm.add_node(daft.Node("sky", r"sky", ph_x + 1.5, ph_y + 2))
pgm.add_edge("sky", "Iadt")

# stars
star_x, star_y = 2., 6.
pgm.add_plate(daft.Plate([star_x - 0.5, star_y - 0.6, 2., 2.], label="stars $n$"))
pgm.add_node(daft.Node("star adt", r"$I_{\nu,n}(\alpha,\delta,t)$", star_x + 0.5, star_y + 0, aspect=verywide))
pgm.add_edge("star adt", "Iadt")
pgm.add_node(daft.Node("star L", r"$L_{\nu,n}(t)$", star_x + 1, star_y + 1, aspect=wide))
pgm.add_edge("star L", "star adt")
pgm.add_node(daft.Node("star pos", r"$\vec{x_n}$", star_x, star_y + 1))
pgm.add_edge("star pos", "star adt")

# done
pgm.render()
pgm.figure.savefig("galex.pdf")
pgm.figure.savefig("galex.png", dpi=150)
