import itertools

import daft
from matplotlib.testing.decorators import image_comparison


@image_comparison(baseline_images=["bca"], extensions=["png"])
def test_bca():
    pgm = daft.PGM()
    pgm.add_node("a", r"$a$", 1, 5)
    pgm.add_node("b", r"$b$", 1, 4)
    pgm.add_node("c", r"$c_n$", 1, 3, observed=True)
    pgm.add_plate([0.5, 2.25, 1, 1.25], label=r"data $n$")
    pgm.add_edge("a", "b")
    pgm.add_edge("b", "c")
    pgm.render()


@image_comparison(baseline_images=["classic"], extensions=["png"])
def test_classic():
    pgm = daft.PGM()

    # Hierarchical parameters.
    pgm.add_node("alpha", r"$\alpha$", 0.5, 2, fixed=True)
    pgm.add_node("beta", r"$\beta$", 1.5, 2)

    # Latent variable.
    pgm.add_node("w", r"$w_n$", 1, 1)

    # Data.
    pgm.add_node("x", r"$x_n$", 2, 1, observed=True)

    # Add in the edges.
    pgm.add_edge("alpha", "beta")
    pgm.add_edge("beta", "w")
    pgm.add_edge("w", "x")
    pgm.add_edge("beta", "x")

    # And a plate.
    pgm.add_plate([0.5, 0.5, 2, 1], label=r"$n = 1, \cdots, N$", shift=-0.1)

    pgm.render()


@image_comparison(baseline_images=["deconvolution"], extensions=["png"])
def test_deconvolution():
    scale = 1.6
    pgm = daft.PGM()

    # Add Nodes
    pgm.add_node("beta dP", r"$\beta_{p}$", 1, 1, scale)
    pgm.add_node("pwf_cr", r"$\Delta p_{cr}$", 2.25, 1, scale)

    pgm.add_node("beta qD", r"$\beta_{q}$", 1, 0, scale)
    pgm.add_node("q_cp", r"$q_{cp}$", 2.25, 0.0, scale)

    pgm.add_node(
        "pwf_prime_obs",
        r"$\frac{d}{dt}\,\Delta p$",
        2.25,
        -1,
        scale,
        alternate=True,
    )
    pgm.add_node(
        "q_prime_obs", r"$\frac{d}{dt}\,q$", 2.25, 2, scale, alternate=True
    )

    pgm.add_node(
        "pwf_conv",
        r"$\Delta p$",
        3.5,
        1.5,
        scale,
        alternate=True,
        plot_params={"ec": "red"},
    )

    pgm.add_node(
        "q_conv",
        r"$q$",
        3.5,
        -0.5,
        scale,
        alternate=True,
        plot_params={"ec": "blue"},
    )

    pgm.add_node(
        "t_conv",
        r"$t$",
        3.5,
        0.5,
        scale,
        alternate=True,
        plot_params={"ec": "orange"},
    )

    # Add Plates
    pgm.add_plate(
        [1.625 - 0.05, -1.5 - 0.025, 1.25, 2], rect_params={"ec": "blue"}
    )
    pgm.add_plate([1.625, -0.5, 1.25, 2], rect_params={"ec": "orange"})
    pgm.add_plate(
        [1.625 + 0.05, 0.5 + 0.025, 1.25, 2], rect_params={"ec": "red"}
    )

    # Add Connections
    pgm.add_edge("beta dP", "pwf_cr")

    pgm.add_edge("beta qD", "q_cp")

    pgm.add_edge("pwf_prime_obs", "q_conv")
    pgm.add_edge("q_prime_obs", "pwf_conv")
    pgm.add_edge("pwf_cr", "pwf_conv")
    pgm.add_edge("q_cp", "q_conv")

    pgm.add_edge("pwf_cr", "t_conv")
    pgm.add_edge("q_cp", "t_conv")

    # Legend
    x0 = -3.75
    pgm.add_node("latent", "", x0 - 0.5, -0.4, 1)
    pgm.add_text(x0 - 0.225, -0.4 - 0.08, "= latent variable")
    pgm.add_node("observed", "", x0 - 0.5, -1.05, 1, alternate=True)
    pgm.add_text(x0 - 0.225, -1.05 - 0.08, "= observed variable")

    x0 -= 0.24
    dx = -0.4
    y0 = 1.8
    dy = -0.35
    pgm.add_text(x0 + dx, y0 + 0 * dy, r"$\beta_{p_{cr}}$")
    pgm.add_text(
        x0, y0 + 0 * dy, "= beta-derivative of constant-rate pressure drop"
    )
    pgm.add_text(x0 + dx, y0 + 1 * dy, r"$\beta_{q_{cp}}$")
    pgm.add_text(
        x0, y0 + 1 * dy, "= beta-derivative of constant-pressure drop rate"
    )
    pgm.add_text(x0 + dx, y0 + 2 * dy, r"$p_{cr}$")
    pgm.add_text(x0, y0 + 2 * dy, "= constant-rate pressure drop function")
    pgm.add_text(x0 + dx, y0 + 3 * dy, r"$q_{cp}$")
    pgm.add_text(x0, y0 + 3 * dy, "= constant-pressure drop rate function")
    pgm.add_text(x0 + dx, y0 + 4 * dy, r"$q$")
    pgm.add_text(x0, y0 + 4 * dy, "= production rate")
    pgm.add_text(x0 + dx, y0 + 5 * dy, r"$\Delta p$")
    pgm.add_text(x0, y0 + 5 * dy, "= pressure drop at sandface")

    # Render and save.
    pgm.render()


@image_comparison(baseline_images=["exoplanets"], extensions=["png"])
def test_exoplanets():
    # Colors.
    p_color = {"ec": "#46a546"}
    s_color = {"ec": "#f89406"}

    pgm = daft.PGM()

    n = daft.Node("phi", r"$\phi$", 1, 3, plot_params=s_color)
    n.va = "baseline"
    pgm.add_node(n)
    pgm.add_node("speckle_coeff", r"$z_i$", 2, 3, plot_params=s_color)
    pgm.add_node("speckle_img", r"$x_i$", 2, 2, plot_params=s_color)

    pgm.add_node("spec", r"$s$", 4, 3, plot_params=p_color)
    pgm.add_node("shape", r"$g$", 4, 2, plot_params=p_color)
    pgm.add_node("planet_pos", r"$\mu_i$", 3, 3, plot_params=p_color)
    pgm.add_node("planet_img", r"$p_i$", 3, 2, plot_params=p_color)

    pgm.add_node("pixels", r"$y_i ^j$", 2.5, 1, observed=True)

    # Edges.
    pgm.add_edge("phi", "speckle_coeff")
    pgm.add_edge("speckle_coeff", "speckle_img")
    pgm.add_edge("speckle_img", "pixels")

    pgm.add_edge("spec", "planet_img")
    pgm.add_edge("shape", "planet_img")
    pgm.add_edge("planet_pos", "planet_img")
    pgm.add_edge("planet_img", "pixels")

    # And a plate.
    pgm.add_plate([1.5, 0.2, 2, 3.2], label=r"exposure $i$", shift=-0.1)
    pgm.add_plate([2, 0.5, 1, 1], label=r"pixel $j$", shift=-0.1)

    # Render and save.
    pgm.render()


@image_comparison(baseline_images=["fixed"], extensions=["png"])
def test_fixed():
    pgm = daft.PGM(aspect=1.5, node_unit=1.75)
    pgm.add_node("unobs", r"Unobserved!", 1, 4)
    pgm.add_node("obs", r"Observed!", 1, 3, observed=True)
    pgm.add_node("alt", r"Alternate!", 1, 2, alternate=True)
    pgm.add_node(
        "fixed", r"Fixed!", 1, 1, fixed=True, aspect=1.0, offset=[0, 5]
    )
    pgm.render()


@image_comparison(baseline_images=["gaia"], extensions=["png"])
def test_gaia():
    pgm = daft.PGM()
    pgm.add_node("omega", r"$\omega$", 2, 5)
    pgm.add_node("true", r"$\tilde{X}_n$", 2, 4)
    pgm.add_node("obs", r"$X_n$", 2, 3, observed=True)
    pgm.add_node("alpha", r"$\alpha$", 3, 4)
    pgm.add_node("Sigma", r"$\Sigma$", 0, 3)
    pgm.add_node("sigma", r"$\sigma_n$", 1, 3)
    pgm.add_plate([0.5, 2.25, 2, 2.25], label=r"stars $n$")
    pgm.add_edge("omega", "true")
    pgm.add_edge("true", "obs")
    pgm.add_edge("alpha", "true")
    pgm.add_edge("Sigma", "sigma")
    pgm.add_edge("sigma", "obs")
    pgm.render()


@image_comparison(baseline_images=["galex"], extensions=["png"])
def test_galex():
    pgm = daft.PGM()
    wide = 1.5
    verywide = 1.5 * wide
    dy = 0.75

    # electrons
    el_x, el_y = 2.0, 2.0
    pgm.add_plate(
        [el_x - 0.6, el_y - 0.6, 2.2, 2 * dy + 0.3], label="electrons $i$"
    )
    pgm.add_node(
        "xabc",
        r"xa$_i$,xabc$_i$,ya$_i$,\textit{etc}",
        el_x + 0.5,
        el_y + 0 * dy,
        aspect=2.3 * wide,
        observed=True,
    )
    pgm.add_node(
        "xyti", r"$x_i,y_i,t_i$", el_x + 1.0, el_y + 1 * dy, aspect=wide
    )
    pgm.add_edge("xyti", "xabc")

    # intensity fields
    ph_x, ph_y = el_x + 2.5, el_y + 3 * dy
    pgm.add_node("Ixyt", r"$I_{\nu}(x,y,t)$", ph_x, ph_y, aspect=verywide)
    pgm.add_edge("Ixyt", "xyti")
    pgm.add_node(
        "Ixnt", r"$I_{\nu}(\xi,\eta,t)$", ph_x, ph_y + 1 * dy, aspect=verywide
    )
    pgm.add_edge("Ixnt", "Ixyt")
    pgm.add_node(
        "Iadt",
        r"$I_{\nu}(\alpha,\delta,t)$",
        ph_x,
        ph_y + 2 * dy,
        aspect=verywide,
    )
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
    pgm.add_plate(
        [star_x - 0.6, star_y - 0.6, 2.2, 2 * dy + 0.3], label="stars $n$"
    )
    pgm.add_node(
        "star adt",
        r"$I_{\nu,n}(\alpha,\delta,t)$",
        star_x + 0.5,
        star_y + 1 * dy,
        aspect=verywide,
    )
    pgm.add_edge("star adt", "Iadt")
    pgm.add_node("star L", r"$L_{\nu,n}(t)$", star_x + 1, star_y, aspect=wide)
    pgm.add_edge("star L", "star adt")
    pgm.add_node("star pos", r"$\vec{x_n}$", star_x, star_y)
    pgm.add_edge("star pos", "star adt")

    # done
    pgm.render()


@image_comparison(baseline_images=["huey_p_newton"], extensions=["png"])
def test_huey_p_newton():
    pgm = daft.PGM()

    kx, ky = 1.5, 1.0
    nx, ny = kx + 3.0, ky + 0.0
    hx, hy, dhx = kx - 0.5, ky + 1.0, 1.0

    pgm.add_node("dyn", r"$\theta_{{dyn}}$", hx + 0.0 * dhx, hy + 0.0)
    pgm.add_node("ic", r"$\theta_{{I.C.}}$", hx + 1.0 * dhx, hy + 0.0)
    pgm.add_node("sun", r"$\theta_{\odot}$", hx + 2.0 * dhx, hy + 0.0)
    pgm.add_node("bg", r"$\theta_{{bg}}$", hx + 3.0 * dhx, hy + 0.0)
    pgm.add_node("Sigma", r"$\Sigma^2$", hx + 4.0 * dhx, hy + 0.0)

    pgm.add_plate([kx - 0.5, ky - 0.6, 2.0, 1.1], label=r"model points $k$")
    pgm.add_node("xk", r"$x_k$", kx + 0.0, ky + 0.0)
    pgm.add_edge("dyn", "xk")
    pgm.add_edge("ic", "xk")
    pgm.add_node("yk", r"$y_k$", kx + 1.0, ky + 0.0)
    pgm.add_edge("sun", "yk")
    pgm.add_edge("xk", "yk")

    pgm.add_plate([nx - 0.5, ny - 0.6, 2.0, 1.1], label=r"data points $n$")
    pgm.add_node("sigman", r"$\sigma^2_n$", nx + 1.0, ny + 0.0, observed=True)
    pgm.add_node("Yn", r"$Y_n$", nx + 0.0, ny + 0.0, observed=True)
    pgm.add_edge("bg", "Yn")
    pgm.add_edge("Sigma", "Yn")
    pgm.add_edge("Sigma", "Yn")
    pgm.add_edge("yk", "Yn")
    pgm.add_edge("sigman", "Yn")

    # Render and save.
    pgm.render()


@image_comparison(baseline_images=["logo"], extensions=["png"])
def test_logo():
    pgm = daft.PGM()
    pgm.add_node("d", r"$D$", 0.5, 0.5)
    pgm.add_node("a", r"$a$", 1.5, 0.5, observed=True)
    pgm.add_node("f", r"$f$", 2.5, 0.5)
    pgm.add_node("t", r"$t$", 3.5, 0.5)
    pgm.add_edge("d", "a")
    pgm.add_edge("a", "f")
    pgm.add_edge("f", "t")
    pgm.render()


@image_comparison(baseline_images=["mrf"], extensions=["png"])
def test_mrf():
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

    pgm.render()


@image_comparison(baseline_images=["no_circles"], extensions=["png"])
def test_no_circles():
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


@image_comparison(baseline_images=["no_gray"], extensions=["png"])
def test_no_gray():
    pgm = daft.PGM(observed_style="inner")

    # Hierarchical parameters.
    pgm.add_node("alpha", r"$\alpha$", 0.5, 2, fixed=True)
    pgm.add_node("beta", r"$\beta$", 1.5, 2)

    # Latent variable.
    pgm.add_node("w", r"$w_n$", 1, 1)

    # Data.
    pgm.add_node("x", r"$x_n$", 2, 1, observed=True)

    # Add in the edges.
    pgm.add_edge("alpha", "beta")
    pgm.add_edge("beta", "w")
    pgm.add_edge("w", "x")
    pgm.add_edge("beta", "x")

    # And a plate.
    pgm.add_plate([0.5, 0.5, 2, 1], label=r"$n = 1, \ldots, N$", shift=-0.1)

    # Render and save.
    pgm.render()


@image_comparison(baseline_images=["recursive"], extensions=["png"])
def test_recursive():
    def recurse(pgm, nodename, level, c):
        if level > 4:
            return nodename
        r = c // 2
        r1nodename = f"r{level:02d}{r:04d}"
        if 2 * r == c:
            # print("adding {0}".format(r1nodename))
            pgm.add_node(
                r1nodename,
                r"reduce",
                2**level * (r + 0.5) - 0.5,
                3 - 0.7 * level,
                aspect=1.9,
            )
        pgm.add_edge(nodename, r1nodename)
        if 2 * r == c:
            return recurse(pgm, r1nodename, level + 1, r)

    pgm = daft.PGM()

    pgm.add_node(
        "query",
        r'"kittens?"',
        3,
        6.0,
        aspect=3.0,
        plot_params={"ec": "none"},
    )
    pgm.add_node("input", r"input", 7.5, 6.0, aspect=3.0)
    pgm.add_edge("query", "input")

    for c in range(16):
        nodename = f"map {c:02d}"
        pgm.add_node(nodename, str(nodename), c, 3.0, aspect=1.9)
        pgm.add_edge("input", nodename)
        level = 1
        recurse(pgm, nodename, level, c)

    pgm.add_node("output", r"output", 7.5, -1.0, aspect=3.0)
    pgm.add_edge("r040000", "output")
    pgm.add_node(
        "answer",
        r'"http://dwh.gg/"',
        12.0,
        -1.0,
        aspect=4.5,
        plot_params={"ec": "none"},
    )
    pgm.add_edge("output", "answer")

    pgm.render()


@image_comparison(baseline_images=["thick_lines"], extensions=["png"])
def test_thick_lines():
    pgm = daft.PGM(line_width=2.5)

    # Hierarchical parameters.
    pgm.add_node("alpha", r"$\alpha$", 0.5, 2, fixed=True)
    pgm.add_node("beta", r"$\beta$", 1.5, 2)

    # Latent variable.
    pgm.add_node("w", r"$w_n$", 1, 1)

    # Data.
    pgm.add_node("x", r"$x_n$", 2, 1, observed=True)

    # Add in the edges.
    pgm.add_edge("alpha", "beta")
    pgm.add_edge("beta", "w")
    pgm.add_edge("w", "x")
    pgm.add_edge("beta", "x")

    # And a plate.
    pgm.add_plate([0.5, 0.5, 2, 1], label=r"$n = 1, \cdots, N$", shift=-0.1)

    # Render and save.
    pgm.render()


@image_comparison(baseline_images=["weaklensing"], extensions=["png"])
def test_weaklensing():
    pgm = daft.PGM()
    pgm.add_node("Omega", r"$\Omega$", -1, 4)
    pgm.add_node("gamma", r"$\gamma$", 0, 4)
    pgm.add_node("obs", r"$\epsilon^{\mathrm{obs}}_n$", 1, 4, observed=True)
    pgm.add_node("alpha", r"$\alpha$", 3, 4)
    pgm.add_node("true", r"$\epsilon^{\mathrm{true}}_n$", 2, 4)
    pgm.add_node("sigma", r"$\sigma_n$", 1, 3)
    pgm.add_node("Sigma", r"$\Sigma$", 0, 3)
    pgm.add_node("x", r"$x_n$", 2, 3, observed=True)
    pgm.add_plate([0.5, 2.25, 2, 2.25], label=r"galaxies $n$")
    pgm.add_edge("Omega", "gamma")
    pgm.add_edge("gamma", "obs")
    pgm.add_edge("alpha", "true")
    pgm.add_edge("true", "obs")
    pgm.add_edge("x", "obs")
    pgm.add_edge("Sigma", "sigma")
    pgm.add_edge("sigma", "obs")
    pgm.render()


@image_comparison(baseline_images=["wordy"], extensions=["png"])
def test_wordy():
    pgm = daft.PGM()
    pgm.add_node("cloudy", r"cloudy", 3, 3, aspect=1.8)
    pgm.add_node("rain", r"rain", 2, 2, aspect=1.2)
    pgm.add_node("sprinkler", r"sprinkler", 4, 2, aspect=2.1)
    pgm.add_node("wet", r"grass wet", 3, 1, aspect=2.4, observed=True)
    pgm.add_edge(
        "cloudy",
        "rain",
        label=r"65%",
        xoffset=-0.1,
        label_params={"rotation": 45},
    )
    pgm.add_edge(
        "cloudy",
        "sprinkler",
        label=r"35%",
        xoffset=0.1,
        label_params={"rotation": -45},
    )
    pgm.add_edge("rain", "wet")
    pgm.add_edge("sprinkler", "wet")
    pgm.render()


@image_comparison(baseline_images=["wordy"], extensions=["png"])
def test_wordy():
    pgm = daft.PGM()
    pgm.add_node("obs", r"$\epsilon^{obs}_n$", 2, 3, observed=True)
    pgm.add_node("true", r"$\epsilon^{true}_n$", 1, 3)
    pgm.add_edge("true", "obs")
    pgm.add_node("alpha", r"$\alpha,\beta$", -0.25, 3)
    pgm.add_edge("alpha", "true")
    pgm.add_node("shape prior", r"$p(\alpha, \beta)$", -1.25, 3, fixed=True)
    pgm.add_edge("shape prior", "alpha")
    pgm.add_node("gamma", r"$\gamma_m$", 2, 4)
    pgm.add_edge("gamma", "obs")
    pgm.add_node("gamma prior", r"$p(\gamma)$", -0.25, 4, fixed=True)
    pgm.add_edge("gamma prior", "gamma")
    pgm.add_node("sigma", r"$\sigma_{\epsilon}$", 3.25, 3, fixed=True)
    pgm.add_edge("sigma", "obs")
    pgm.add_plate([0.5, 2.25, 2, 1.25], label=r"galaxies $n$")
    pgm.add_plate([0.25, 1.75, 2.5, 2.75], label=r"patches $m$")
    pgm.render()
