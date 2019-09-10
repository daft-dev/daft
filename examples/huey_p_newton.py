"""
n-body particle inference
=========================

Dude.
"""

import daft
from matplotlib import rc

rc("font", family="serif", size=12)
rc("text", usetex=True)


pgm = daft.PGM()

kx, ky = 1.5, 1.0
nx, ny = kx + 3.0, ky + 0.0
hx, hy, dhx = kx - 0.5, ky + 1.0, 1.0

pgm.add_node("dyn", r"$\theta_{\mathrm{dyn}}$", hx + 0.0 * dhx, hy + 0.0)
pgm.add_node("ic", r"$\theta_{\mathrm{I.C.}}$", hx + 1.0 * dhx, hy + 0.0)
pgm.add_node("sun", r"$\theta_{\odot}$", hx + 2.0 * dhx, hy + 0.0)
pgm.add_node("bg", r"$\theta_{\mathrm{bg}}$", hx + 3.0 * dhx, hy + 0.0)
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
pgm.savefig("huey_p_newton.pdf")
pgm.savefig("huey_p_newton.png", dpi=150)
