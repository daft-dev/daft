Daft
====

.. raw:: html

    <div id="examples-block"></div>
    <div id="more-examples" style="text-align: right;font-size: 0.8em;">
        <a href="examples">More…</a>
    </div>
    <script src="_static/examples.js?v=2"></script>
    <script>
        show_examples("_images", "_static", "examples", 6);
    </script>


Summary
-------

**Daft** is a Python package that uses `matplotlib <http://matplotlib.org/>`_
to render pixel-perfect *probabilistic graphical models* for publication
in a journal or on the internet. With a short Python script and an intuitive
model-building syntax you can design directed (Bayesian Networks, directed
acyclic graphs) and undirected (Markov random fields) models and save
them in any formats that matplotlib supports (including PDF, PNG, EPS and
SVG).


Installation
------------

Installing the most recent stable version of Daft should be pretty easy
if you use `pip <http://www.pip-installer.org>`_:

.. code-block:: bash

    python -m pip install daft

Otherwise, you can download the source and run:

.. code-block:: bash

    python -m pip install -e .

in the root directory.

Daft only depends on `matplotlib <http://matplotlib.org/>`_ and
`numpy <http://numpy.scipy.org>`_. These are standard components of the
scientific Python stack but if you don't already have them installed ``pip``
will try to install them for you.


Issues
------

If you have any problems or questions, `open an "issue" on Github
<https://github.com/daft-dev/daft/issues>`_.


Authors & Contributions
-----------------------

**Daft** is being developed and supported by `David S. Fulford
<https://github.com/dsfulf>`_, `Dan Foreman-Mackey
<https://dfm.io>`_ and `David W. Hogg <http://cosmo.nyu.edu/hogg>`_.

For the hackers in the house, development happens on `Github
<https://github.com/daft-dev/daft>`_ and we welcome pull requests. In particular,
we'd love to see examples of how you're using Daft in your work.


License
-------

*Copyright 2012-2021 Daft Developers.*

**Daft** is free software made available under the *MIT License*. For details
see `the LICENSE file <https://raw.github.com/daft-dev/daft/master/LICENSE.rst>`_.

If you use Daft in academic projects, acknowledgements are greatly
appreciated.


API
---

.. toctree::
   :maxdepth: 2

   api
   examples/index
