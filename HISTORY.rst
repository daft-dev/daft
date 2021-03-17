.. :changelog:

0.1.2 (2020-04-10)
++++++++++++++++++

- Maintenance release for compatibility with numpy and matplotlib
- Updates documentation and improves unit testing


0.1.1 (2020-04-10)
++++++++++++++++++

- Fix bug where ``pgm.savefig()`` is called before ``pmg.render()``.


0.1.0 (2019-09-16)
++++++++++++++++++

- Auto-sizing of plot. No longer any need to explicitly declare size or origin.
- Remove need to declare :class:`Node`, :class:`Edge`, or :class:`Plate` classes when calling
  ``add_node()``, ``add_edge``, or ``add_plate``. Should simplify syntax.
- Can now style (offset, rotation) :class:`Edge` annotations as ``label`` param, additional
  parameters passed through as ``label_params`` to :class:`matplotlib.axes.Axes.annotate`.
- Add `alternative` node style as an option for unobserved parameters.
- Fix default ``bbox`` ``facecolor`` to be 'none'.
- Fix various ``dict`` params when default is ``None``.
- Fix types of passed params to ensure cast to ``float``.
- Update examples and documentation. Documentation will now auto-build by Travis.


0.0.4 (2016-03-14)
++++++++++++++++++

- Added ``bbox`` dict to :class:`Plate` which is passed as kwargs to
  :class:`matplotlib.axes.Axes.annotate`
- Fixes for Python3 dictionaries
- Fix bug about zero-length :class:`Edge`
- Add rectangle shape for :class:`Node`
- Add ``numpy`` and ``matplotlib`` to dependencies
- Add basic :class:`Edge` annotations
- Set more default params


0.0.3 (2012-10-04)
++++++++++++++++++

- Fixed rendering bug when ``aspect`` was used with angles other than 45 degrees between nodes.
- Added global ``aspect`` property to the rendering context.
- Fixed the treatment of redundant keyword arguments that ``matplotlib` allows.


0.0.2 (2012-09-28)
++++++++++++++++++

- Initial release.
