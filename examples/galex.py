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
pgm = daft.PGM([7.0, 5.5], origin=[0.5, 1.2])

# electrons
el_x, el_y = 2., 2.
pgm.add_plate(daft.Plate([el_x - 0.5, el_y - 0.6, 2., 2.], label="electrons $i$"))
pgm.add_node(daft.Node("raw6", r"raw6$_i$", el_x + 1, el_y, aspect=1.5, observed=True))
pgm.add_node(daft.Node("xyti", r"$x_i,y_i,t_i$", el_x + 1, el_y + 1, aspect=1.5))
pgm.add_edge("xyti", "raw6")

# photons
ph_x, ph_y = 5., 3.
pgm.add_plate(daft.Plate([ph_x - 0.5, ph_y - 0.6, 2., 2.], label="photons"))
pgm.add_node(daft.Node("photon xy", r"$x,y$", ph_x, ph_y))
pgm.add_edge("photon xy", "xyti")
pgm.add_node(daft.Node("photon tp", r"$\xi,\eta$", ph_x + 1, ph_y + 1))
pgm.add_edge("photon tp", "photon xy")
pgm.add_node(daft.Node("photon adt", r"$\alpha,\delta,t$", ph_x, ph_y + 1, aspect=1.5))
pgm.add_edge("photon adt", "photon tp")
pgm.add_edge("photon adt", "xyti")

# s/c
pgm.add_node(daft.Node("wha", r"?", 1, 2))
pgm.add_edge("wha", "raw6")
pgm.add_node(daft.Node("fee", r"fee", 1, 3))
pgm.add_edge("fee", "xyti")
pgm.add_node(daft.Node("dark", r"dark", 4, 2, aspect=1.5))
pgm.add_edge("dark", "xyti")
pgm.add_node(daft.Node("att", r"att", 7, 4))
pgm.add_edge("att", "photon tp")
pgm.add_node(daft.Node("optics", r"optics", 7, 3, aspect=1.5))
pgm.add_edge("optics", "photon xy")
pgm.add_node(daft.Node("psf", r"psf", 7, 2))
pgm.add_edge("psf", "photon xy")

# stars
star_x, star_y = 2., 5.
pgm.add_plate(daft.Plate([star_x - 0.5, star_y - 0.6, 2., 2.], label="stars"))
pgm.add_node(daft.Node("star ad", r"$\alpha,\delta$", star_x + 1, star_y + 0))
pgm.add_edge("star ad", "photon adt")
pgm.add_node(daft.Node("star f", r"$f_{\lambda}(t)$", star_x + 1, star_y + 1))
pgm.add_edge("star f", "photon adt")
pgm.add_node(daft.Node("star pars", r"$\omega$", star_x, star_y + 1))
pgm.add_edge("star pars", "star f")

# sky
pgm.add_node(daft.Node("sky", r"sky", 5, 5))
pgm.add_edge("sky", "photon adt")

# done
pgm.render()
pgm.figure.savefig("galex.pdf")
pgm.figure.savefig("galex.png", dpi=150)
