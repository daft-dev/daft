"""
Bayesian Deconvolution
======================

This is Fulford's model for simultaneous inversion of the constant-rate
pressure function and constant-pressure rate function for variable-rate
variable-pressure fluid flow through porous media.

"""

import daft

scale = 1.6
pgm = daft.PGM()


# Define helper functions
def text_plate(x0, y0, text):
    pgm.add_plate([x0, y0, 0., 0.], label=text, rect_params={'ec': 'none'})


def conv_plate(x0, y0, width, height, color):
    pgm.add_plate([x0, y0, 1.25, 2.], rect_params={'fc': 'none'})
    pgm.add_plate([x0, y0, 1.25, 2.], rect_params={'ec': color})


def comp_plate(x0, y0, width, height, color):
    pgm.add_plate([x0, y0, width, height], rect_params={'ec': color})


# Add Nodes
pgm.add_node('beta dP', r'$\beta_{p}$', 1, 1, scale)
pgm.add_node('pwf_cr', r'$\Delta p_{cr}$', 2.25, 1, scale)

pgm.add_node('beta qD', r'$\beta_{q}$', 1, 0, scale)
pgm.add_node('q_cp', r'$q_{cp}$', 2.25, 0., scale)

pgm.add_node('pwf_prime_obs', r'$\frac{d}{dt}\,\Delta p$', 2.25, -1, scale, alternate=True)
pgm.add_node('q_prime_obs', r'$\frac{d}{dt}\,q$', 2.25, 2, scale, alternate=True)

pgm.add_node('pwf_conv', r'$\Delta p$', 3.5, 1.5, scale, alternate=True, plot_params={'ec': 'red'})

pgm.add_node('q_conv', r'$q$', 3.5, -.5, scale, alternate=True, plot_params={'ec': 'blue'})

pgm.add_node('t_conv', r'$t$', 3.5, .5, scale, alternate=True, plot_params={'ec': 'orange'})


conv_plate(x0=1.625-.05, y0=-1.5-.025, width=1.25, height=2, color='blue')
conv_plate(x0=1.625,     y0=-.5,       width=1.25, height=2, color='orange')
conv_plate(x0=1.625+.05, y0=0.5+.025,  width=1.25, height=2, color='red')


# Add Connections
pgm.add_edge('beta dP', 'pwf_cr')

pgm.add_edge('beta qD', 'q_cp')

pgm.add_edge('pwf_prime_obs', 'q_conv')
pgm.add_edge('q_prime_obs', 'pwf_conv')
pgm.add_edge('pwf_cr', 'pwf_conv')
pgm.add_edge('q_cp', 'q_conv')

pgm.add_edge('pwf_cr', 't_conv')
pgm.add_edge('q_cp', 't_conv')

# Legend
x0 = -3.75
pgm.add_node('latent', '', x0-.5, -0.4, 1)
text_plate(x0-.25, -.4-.125, '= latent variable')
pgm.add_node('observed', '', x0-.5, -1.05, 1, alternate=True)
text_plate(x0-.25, -1.05-.125, '= observed variable')

x0 -= .25
dx = -.4
y0 = 1.8
dy = -.35
text_plate(x0+dx, y0+0*dy, r'$\beta_{p_{cr}}$')
text_plate(x0, y0+0*dy, '= beta-derivative of constant-rate pressure drop')
text_plate(x0+dx, y0+1*dy, r'$\beta_{q_{cp}}$')
text_plate(x0, y0+1*dy, '= beta-derivative of constant-pressure drop rate')
text_plate(x0+dx, y0+2*dy, r'$p_{cr}$')
text_plate(x0, y0+2*dy, '= constant-rate pressure drop function')
text_plate(x0+dx, y0+3*dy, r'$q_{cp}$')
text_plate(x0, y0+3*dy, '= constant-pressure drop rate function')
text_plate(x0+dx, y0+4*dy, r'$q$')
text_plate(x0, y0+4*dy, '= production rate')
text_plate(x0+dx, y0+5*dy, r'$\Delta p$')
text_plate(x0, y0+5*dy, '= pressure drop at sandface')

# Render and save.
pgm.render()
pgm.savefig('deconvolution.pdf')
pgm.savefig('deconvolution.png', dpi=150)
