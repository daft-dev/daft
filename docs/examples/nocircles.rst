.. _nocircles:


Nodes can go free
=================

.. figure:: /_static/examples/nocircles.png


Nodes can go free
=================

You don't need to put ellipses or circles around your node contents,
if you don't want to.



::

    
    from matplotlib import rc
    rc("font", family="serif", size=12)
    rc("text", usetex=True)
    
    import daft
    
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
    pgm.savefig("nocircles.pdf")
    pgm.savefig("nocircles.png", dpi=150)
    

