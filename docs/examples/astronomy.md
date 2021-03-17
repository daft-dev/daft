---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

Astronomical imaging
====================

This is a model for every pixel of every astronomical image ever
taken.  It is incomplete!

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

pgm = daft.PGM(grid_unit=4.0, node_unit=1.4)

# Start with the plates.
tweak = 0.02
rect_params = {"lw": 2}
pgm.add_plate(
    [1.5 + tweak, 0.5 + tweak, 6.0 - 2 * tweak, 3.75 - 2 * tweak],
    label=r"\Large telescope+camera+filter multiplets",
    rect_params=rect_params,
)
pgm.add_plate(
    [2.5 + tweak, 1.0 + tweak, 4.0 - 2 * tweak, 2.75 - 2 * tweak],
    label=r"\Large images",
    rect_params=rect_params,
)
pgm.add_plate(
    [3.5 + tweak, 1.5 + tweak, 2.0 - 2 * tweak, 1.75 - 2 * tweak],
    label=r"\Large pixel patches",
    rect_params=rect_params,
)
pgm.add_plate(
    [1.0 + tweak, 4.25 + tweak, 3.5 - 2 * tweak, 1.75 - 2 * tweak],
    label=r"\Large stars",
    rect_params=rect_params,
)
pgm.add_plate(
    [5.5 + tweak, 4.25 + tweak, 2.5 - 2 * tweak, 1.75 - 2 * tweak],
    label=r"\Large galaxies",
    rect_params=rect_params,
)

# ONLY pixels are observed
asp = 2.3
pgm.add_node("true pixels", r"~\\noise-free\\pixel patch", 5.0, 2.5, aspect=asp)
pgm.add_node("pixels", r"pixel patch", 4.0, 2.0, observed=True, aspect=asp)
pgm.add_edge("true pixels", "pixels")

# The sky
pgm.add_node("sky", r"sky model", 6.0, 2.5, aspect=asp)
pgm.add_edge("sky", "true pixels")
pgm.add_node("sky prior", r"sky priors", 8.0, 2.5, fixed=True)
pgm.add_edge("sky prior", "sky")

# Stars
pgm.add_node("star patch", r"star patch", 4.0, 3.0, aspect=asp)
pgm.add_edge("star patch", "true pixels")
pgm.add_node("star SED", r"~\\spectral energy\\distribution", 2.5, 4.75, aspect=asp + 0.2)
pgm.add_edge("star SED", "star patch")
pgm.add_node("star position", r"position", 4.0, 4.75, aspect=asp)
pgm.add_edge("star position", "star patch")
pgm.add_node("temperature", r"temperature", 1.5, 5.25, aspect=asp)
pgm.add_edge("temperature", "star SED")
pgm.add_node("luminosity", r"luminosity", 2.5, 5.25, aspect=asp)
pgm.add_edge("luminosity", "star SED")
pgm.add_node("metallicity", r"metallicity", 1.5, 5.75, aspect=asp)
pgm.add_edge("metallicity", "star SED")
pgm.add_edge("metallicity", "temperature")
pgm.add_edge("metallicity", "luminosity")
pgm.add_node("mass", r"mass", 2.5, 5.75, aspect=asp)
pgm.add_edge("mass", "temperature")
pgm.add_edge("mass", "luminosity")
pgm.add_node("age", r"age", 3.5, 5.75, aspect=asp)
pgm.add_edge("age", "temperature")
pgm.add_edge("age", "luminosity")
pgm.add_node("star models", r"star models", 1.0, 4.0, fixed=True)
pgm.add_edge("star models", "temperature")
pgm.add_edge("star models", "luminosity")
pgm.add_edge("star models", "star SED")

# Galaxies
pgm.add_node("galaxy patch", r"galaxy patch", 5.0, 3.0, aspect=asp)
pgm.add_edge("galaxy patch", "true pixels")
pgm.add_node("galaxy SED", r"~\\spectral energy\\distribution", 6.5, 4.75, aspect=asp + 0.2)
pgm.add_edge("galaxy SED", "galaxy patch")
pgm.add_node("morphology", r"morphology", 7.5, 4.75, aspect=asp)
pgm.add_edge("morphology", "galaxy patch")
pgm.add_node("SFH", r"~\\star-formation\\history", 7.5, 5.25, aspect=asp)
pgm.add_edge("SFH", "galaxy SED")
pgm.add_edge("SFH", "morphology")
pgm.add_node("galaxy position", r"~\\redshift\\ \& position", 6.0, 5.25, aspect=asp)
pgm.add_edge("galaxy position", "galaxy SED")
pgm.add_edge("galaxy position", "morphology")
pgm.add_edge("galaxy position", "galaxy patch")
pgm.add_node("dynamics", r"orbit structure", 6.5, 5.75, aspect=asp)
pgm.add_edge("dynamics", "morphology")
pgm.add_edge("dynamics", "SFH")
pgm.add_node("galaxy mass", r"mass", 7.5, 5.75, aspect=asp)
pgm.add_edge("galaxy mass", "dynamics")
pgm.add_edge("galaxy mass", "galaxy SED")
pgm.add_edge("galaxy mass", "SFH")

# Universals
pgm.add_node("extinction model", r"~\\extinction\\model", 5.0, 4.75, aspect=asp)
pgm.add_edge("extinction model", "star patch")
pgm.add_edge("extinction model", "galaxy patch")
pgm.add_node("MW", r"~\\Milky Way\\formation", 4.0, 6.5, aspect=asp)
pgm.add_edge("MW", "metallicity")
pgm.add_edge("MW", "mass")
pgm.add_edge("MW", "age")
pgm.add_edge("MW", "star position")
pgm.add_edge("MW", "extinction model")
pgm.add_node("galaxy formation", r"~\\galaxy\\formation", 5.0, 6.5, aspect=asp)
pgm.add_edge("galaxy formation", "MW")
pgm.add_edge("galaxy formation", "dynamics")
pgm.add_edge("galaxy formation", "galaxy mass")
pgm.add_edge("galaxy formation", "extinction model")
pgm.add_node("LSS", r"~\\large-scale\\structure", 6.0, 6.5, aspect=asp)
pgm.add_edge("LSS", "galaxy position")
pgm.add_node("cosmology", r"~\\cosmological\\parameters", 6.0, 7.0, aspect=asp)
pgm.add_edge("cosmology", "LSS")
pgm.add_edge("cosmology", "galaxy formation")
pgm.add_node("god", r"God", 7.0, 7.0, fixed=True)
pgm.add_edge("god", "cosmology")

# Sensitivity
pgm.add_node("zeropoint", r"~\\zeropoint\\(photocal)", 3.0, 3.0, aspect=asp)
pgm.add_edge("zeropoint", "true pixels")
pgm.add_node("exposure time", r"exposure time", 3.0, 2.5, observed=True, aspect=asp)
pgm.add_edge("exposure time", "zeropoint")

# The PSF
pgm.add_node("WCS", r"~\\astrometric\\calibration", 3.0, 2.0, aspect=asp)
pgm.add_edge("WCS", "star patch")
pgm.add_edge("WCS", "galaxy patch")
pgm.add_node("psf", r"PSF model", 3.0, 3.5, aspect=asp)
pgm.add_edge("psf", "star patch")
pgm.add_edge("psf", "galaxy patch")
pgm.add_node("optics", r"optics", 2.0, 3.0, aspect=asp - 1.2)
pgm.add_edge("optics", "psf")
pgm.add_edge("optics", "WCS")
pgm.add_node("atmosphere", r"~\\atmosphere\\model", 1.0, 3.5, aspect=asp)
pgm.add_edge("atmosphere", "psf")
pgm.add_edge("atmosphere", "WCS")
pgm.add_edge("atmosphere", "zeropoint")

# The device
pgm.add_node("flatfield", r"flat-field", 2.0, 1.5, aspect=asp)
pgm.add_edge("flatfield", "pixels")
pgm.add_node("nonlinearity", r"non-linearity", 2.0, 1.0, aspect=asp)
pgm.add_edge("nonlinearity", "pixels")
pgm.add_node("pointing", r"~\\telescope\\pointing etc.", 2.0, 2.0, aspect=asp)
pgm.add_edge("pointing", "WCS")
pgm.add_node("detector", r"detector priors", 1.0, 1.5, fixed=True)
pgm.add_edge("detector", "flatfield")
pgm.add_edge("detector", "nonlinearity")
pgm.add_node("hardware", r"hardware priors", 1.0, 2.5, fixed=True)
pgm.add_edge("hardware", "pointing")
pgm.add_edge("hardware", "exposure time")
pgm.add_edge("hardware", "optics")

# Noise
pgm.add_node("noise patch", r"noise patch", 5.0, 2.0, aspect=asp)
pgm.add_edge("noise patch", "pixels")
pgm.add_edge("true pixels", "noise patch")
pgm.add_node("noise model", r"noise model", 7.0, 2.0, aspect=asp)
pgm.add_edge("noise model", "noise patch")
pgm.add_node("noise prior", r"noise priors", 8.0, 2.0, fixed=True)
pgm.add_edge("noise prior", "noise model")
pgm.add_node("cosmic rays", r"~\\cosmic-ray\\model", 8.0, 1.5, aspect=asp)
pgm.add_edge("cosmic rays", "noise patch")

# Render and save.
pgm.render()
```
