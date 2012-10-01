"""
Astronomical imaging
====================

This is a model for every pixel of every astronomical image ever
taken.

"""

from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=True)

import daft

pgm = daft.PGM([8, 8], origin=[0.5, 0.5], grid_unit=4., node_unit=1.4)

# Start with the plates.
tweak=0.01
pgm.add_plate(daft.Plate([1.5+tweak, 0.5+tweak, 6.0-2*tweak, 3.75-2*tweak], label=r"\huge telescope+camera+filter multiplets"))
pgm.add_plate(daft.Plate([2.5+tweak, 1.0+tweak, 4.0-2*tweak, 2.75-2*tweak], label=r"\huge images"))
pgm.add_plate(daft.Plate([3.5+tweak, 1.5+tweak, 2.0-2*tweak, 1.75-2*tweak], label=r"\huge pixel patches"))
pgm.add_plate(daft.Plate([1.5+tweak, 4.25+tweak, 3.0-2*tweak, 1.75-2*tweak], label=r"\huge stars"))
pgm.add_plate(daft.Plate([4.5+tweak, 4.25+tweak, 3.0-2*tweak, 1.75-2*tweak], label=r"\huge galaxies"))

# ONLY pixels are observed
asp = 2.5
pgm.add_node(daft.Node("true pixels", r"~\\noise-free\\pixel patch", 5.0, 2.5, aspect=asp))
pgm.add_node(daft.Node("pixels", r"pixel patch", 4.0, 2.0, observed=True, aspect=asp))
pgm.add_edge("true pixels", "pixels")

# The sky
pgm.add_node(daft.Node("sky", r"sky model", 6.0, 2.5, aspect=asp))
pgm.add_edge("sky", "true pixels")
pgm.add_node(daft.Node("sky prior", r"sky priors", 8.0, 2.5, fixed=True))
pgm.add_edge("sky prior", "sky")

# Stars
pgm.add_node(daft.Node("star patch", r"star patch", 4.0, 3.0, aspect=asp))
pgm.add_edge("star patch", "true pixels")
pgm.add_node(daft.Node("star SED", r"~\\spectral energy\\distribution", 3.0, 4.75, aspect=asp))
pgm.add_edge("star SED", "star patch")
pgm.add_node(daft.Node("star position", r"position", 4.0, 4.75, aspect=asp))
pgm.add_edge("star position", "star patch")
pgm.add_node(daft.Node("temperature", r"temperature", 2.0, 5.25, aspect=asp))
pgm.add_edge("temperature", "star SED")
pgm.add_node(daft.Node("luminosity", r"luminosity", 3.0, 5.25, aspect=asp))
pgm.add_edge("luminosity", "star SED")
pgm.add_node(daft.Node("star extinction", r"extinction", 4.0, 5.25, aspect=asp))
pgm.add_edge("star extinction", "star SED")
pgm.add_edge("star position", "star extinction")
pgm.add_node(daft.Node("metallicity", r"metallicity", 2.0, 5.75, aspect=asp))
pgm.add_edge("metallicity", "star SED")
pgm.add_edge("metallicity", "temperature")
pgm.add_edge("metallicity", "luminosity")
pgm.add_node(daft.Node("mass", r"mass", 3.0, 5.75, aspect=asp))
pgm.add_edge("mass", "temperature")
pgm.add_edge("mass", "luminosity")
pgm.add_node(daft.Node("age", r"age", 4.0, 5.75, aspect=asp))
pgm.add_edge("age", "temperature")
pgm.add_edge("age", "luminosity")

# Galaxies
pgm.add_node(daft.Node("galaxy patch", r"galaxy patch", 5.0, 3.0, aspect=asp))
pgm.add_edge("galaxy patch", "true pixels")
pgm.add_node(daft.Node("galaxy SED", r"~\\spectral energy\\distribution", 6.0, 4.75, aspect=asp))
pgm.add_edge("galaxy SED", "galaxy patch")
pgm.add_node(daft.Node("morphology", r"morphology", 7.0, 4.75, aspect=asp))
pgm.add_edge("morphology", "galaxy patch")
pgm.add_node(daft.Node("galaxy position", r"~\\redshift\\ \& position", 5.0, 5.25, aspect=asp))
pgm.add_edge("galaxy position", "galaxy SED")
pgm.add_edge("galaxy position", "morphology")
pgm.add_edge("galaxy position", "galaxy patch")
pgm.add_node(daft.Node("SFH", r"~\\star-formation\\history", 7.0, 5.25, aspect=asp))
pgm.add_edge("SFH", "galaxy SED")
pgm.add_edge("SFH", "morphology")

# Sensitivity
pgm.add_node(daft.Node("zeropoint", r"~\\zeropoint\\(photocal)", 3.0, 3.0, aspect=asp))
pgm.add_edge("zeropoint", "true pixels")
pgm.add_node(daft.Node("exposure time", r"exposure time", 3.0, 2.5, observed=True, aspect=asp))
pgm.add_edge("exposure time", "zeropoint")

# The PSF
pgm.add_node(daft.Node("psf", r"PSF model", 3.0, 3.5, aspect=asp))
pgm.add_edge("psf", "star patch")
pgm.add_edge("psf", "galaxy patch")
pgm.add_node(daft.Node("optics", r"optics PSF", 2.0, 3.5, aspect=asp))
pgm.add_edge("optics", "psf")
pgm.add_node(daft.Node("atmosphere", r"~\\atmosphere\\model", 1.0, 3.0, aspect=asp))
pgm.add_edge("atmosphere", "psf")
pgm.add_edge("atmosphere", "zeropoint")

# The device
pgm.add_node(daft.Node("flatfield", r"flat-field", 2.0, 1.5, aspect=asp))
pgm.add_edge("flatfield", "pixels")
pgm.add_node(daft.Node("nonlinearity", r"non-linearity", 2.0, 1.0, aspect=asp))
pgm.add_edge("nonlinearity", "pixels")

# Noise
pgm.add_node(daft.Node("noise patch", r"noise patch", 5.0, 2.0, aspect=asp))
pgm.add_edge("noise patch", "pixels")
pgm.add_edge("true pixels", "noise patch")
pgm.add_node(daft.Node("noise model", r"noise model", 7.0, 2.0, aspect=asp))
pgm.add_edge("noise model", "noise patch")
pgm.add_node(daft.Node("noise prior", r"noise priors", 8.0, 2.0, fixed=True))
pgm.add_edge("noise prior", "noise model")
pgm.add_node(daft.Node("cosmic rays", r"cosmic-ray model", 8.0, 1.5, aspect=asp))
pgm.add_edge("cosmic rays", "noise patch")

# Render and save.
pgm.render()
pgm.figure.savefig("astronomy.pdf")
pgm.figure.savefig("astronomy.png", dpi=150)
