"""Code for Daft"""

__all__ = ["PGM", ]
# TODO: should Text be added?

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrow, Rectangle

import numpy as np

from typing import Any
from numpy.typing import NDArray, ArrayLike


from .node import Node
from .edge import Edge
from .plate import Plate, Text
from ._utils import _rendering_context
from ._types import NDArray2, NDArrayF, NDArrayI

# pylint: disable=too-many-arguments, protected-access, unused-argument, too-many-lines


class PGM:
    """
    The base object for building a graphical model representation.

    :param shape: (optional)
        The number of rows and columns in the grid. Will automatically
        determine is not provided.

    :param origin: (optional)
        The coordinates of the bottom left corner of the plot. Will
        automatically determine if not provided.

    :param grid_unit: (optional)
        The size of the grid spacing measured in centimeters.

    :param node_unit: (optional)
        The base unit for the node size. This is a number in centimeters that
        sets the default diameter of the nodes.

    :param observed_style: (optional)
        How should the "observed" nodes be indicated? This must be one of:
        ``"shaded"``, ``"inner"`` or ``"outer"`` where ``inner`` and
        ``outer`` nodes are shown as double circles with the second circle
        plotted inside or outside of the standard one, respectively.

    :param alternate_style: (optional)
        How should the "alternate" nodes be indicated? This must be one of:
        ``"shaded"``, ``"inner"`` or ``"outer"`` where ``inner`` and
        ``outer`` nodes are shown as double circles with the second circle
        plotted inside or outside of the standard one, respectively.

    :param node_ec: (optional)
        The default edge color for the nodes.

    :param node_fc: (optional)
        The default face color for the nodes.

    :param plate_fc: (optional)
        The default face color for plates.

    :param directed: (optional)
        Should the edges be directed by default?

    :param aspect: (optional)
        The default aspect ratio for the nodes.

    :param label_params: (optional)
        Default node label parameters. See :class:`PGM.Node` for details.

    :param dpi: (optional)
        Set DPI for display and saving files.

    """

    def __init__(
        self,
        shape: tuple[float, float] | list[float] | NDArrayF | None = None,
        origin: ArrayLike | None = None,
        grid_unit: float = 2.0,
        node_unit: float = 1.0,
        observed_style: str = "shaded",
        alternate_style: str = "inner",
        line_width: float = 1.0,
        node_ec: str = "k",
        node_fc: str = "w",
        plate_fc: str = "w",
        directed: bool = True,
        aspect: float = 1.0,
        label_params: dict[str, Any] | None = None,
        dpi: int | None = None,
    ) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: dict[str, Edge] = []
        self._plates: dict[str, Plate] = []
        self._dpi = dpi

        # if shape and origin are not given, pass a default
        # and we will determine at rendering time
        self.shape = shape
        self.origin = origin
        if shape is None:
            shape = [1, 1]
        if origin is None:
            origin = [0, 0]

        self._ctx = _rendering_context(
            shape=shape,
            origin=origin,
            grid_unit=grid_unit,
            node_unit=node_unit,
            observed_style=observed_style,
            alternate_style=alternate_style,
            line_width=line_width,
            node_ec=node_ec,
            node_fc=node_fc,
            plate_fc=plate_fc,
            directed=directed,
            aspect=aspect,
            label_params=label_params,
            dpi=dpi,
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._ctx.close()

    def add_node(
        self,
        node,
        content="",
        x=0,
        y=0,
        scale=1.0,
        aspect=None,
        observed=False,
        fixed=False,
        alternate=False,
        offset=(0.0, 0.0),
        fontsize=None,
        plot_params=None,
        label_params=None,
        shape="ellipse",
    ):
        """
        Add a :class:`Node` to the model.

        :param node:
            The plain-text identifier for the nodeself.
            Can also be the :class:`Node` to retain backward compatibility.

        :param content:
            The display form of the variable.

        :param x:
            The x-coordinate of the node in *model units*.

        :param y:
            The y-coordinate of the node.

        :param scale: (optional)
            The diameter (or height) of the node measured in multiples of
            ``node_unit`` as defined by the :class:`PGM` object.

        :param aspect: (optional)
            The aspect ratio width/height for elliptical nodes; default 1.

        :param observed: (optional)
            Should this be a conditioned variable?

        :param fixed: (optional)
            Should this be a fixed (not permitted to vary) variable?
            If `True`, modifies or over-rides ``diameter``, ``offset``,
            ``facecolor``, and a few other ``plot_params`` settings.
            This setting conflicts with ``observed``.

        :param alternate: (optional)
            Should this use the alternate style?

        :param offset: (optional)
            The ``(dx, dy)`` offset of the label (in points) from the default
            centered position.

        :param fontsize: (optional)
            The fontsize to use.

        :param plot_params: (optional)
            A dictionary of parameters to pass to the
            :class:`matplotlib.patches.Ellipse` constructor.

        :param label_params: (optional)
            A dictionary of parameters to pass to the
            :class:`matplotlib.text.Annotation` constructor. Any kwargs not
            used by Annontation get passed to :class:`matplotlib.text.Text`.

        :param shape: (optional)
            String in {ellipse (default), rectangle}
            If rectangle, aspect and scale holds for rectangle

        """
        if isinstance(node, Node):
            _node = node
        else:
            _node = Node(
                node,
                content,
                x,
                y,
                scale,
                aspect,
                observed,
                fixed,
                alternate,
                offset,
                fontsize,
                plot_params,
                label_params,
                shape,
            )

        self._nodes[_node.name] = _node

        return node

    def add_edge(
        self,
        name1,
        name2,
        directed=None,
        xoffset=0.0,
        yoffset=0.1,
        label=None,
        plot_params=None,
        label_params=None,
        **kwargs,  # pylint: disable=unused-argument
    ):
        """
        Construct an :class:`Edge` between two named :class:`Node` objects.

        :param name1:
            The name identifying the first node.

        :param name2:
            The name identifying the second node. If the edge is directed,
            the arrow will point to this node.

        :param directed: (optional)
            Should the edge be directed from ``node1`` to ``node2``? In other
            words: should it have an arrow?

        :param label: (optional)
            A string to annotate the edge.

        :param xoffset: (optional)
            The x-offset from the middle of the arrow to plot the label.
            Only takes effect if `label` is defined in `plot_params`.

        :param yoffset: (optional)
            The y-offset from the middle of the arrow to plot the label.
            Only takes effect if `label` is defined in `plot_params`.

        :param plot_params: (optional)
            A dictionary of parameters to pass to the
            :class:`matplotlib.patches.FancyArrow` constructor.

        :param label_params: (optional)
            A dictionary of parameters to pass to the
            :class:`matplotlib.axes.Axes.annotate` constructor.

        """
        if directed is None:
            directed = self._ctx.directed

        e = Edge(
            self._nodes[name1],
            self._nodes[name2],
            directed=directed,
            label=label,
            xoffset=xoffset,
            yoffset=yoffset,
            plot_params=plot_params,
            label_params=label_params,
        )
        self._edges.append(e)

        return e

    def add_plate(
        self,
        plate,
        label=None,
        label_offset=(5, 5),
        shift=0,
        position="bottom left",
        fontsize=None,
        rect_params=None,
        bbox=None,
    ):
        """
        Add a :class:`Plate` object to the model.

        :param plate:
            The rectangle describing the plate bounds in model coordinates.
            Can also be the :class:`Plate` to retain backward compatibility.

        :param label: (optional)
            A string to annotate the plate.

        :param label_offset: (optional)
            The x and y offsets of the label text measured in points.

        :param shift: (optional)
            The vertical "shift" of the plate measured in model units. This
            will move the bottom of the panel by ``shift`` units.

        :param position: (optional)
            One of ``"{vertical} {horizontal}"`` where vertical is ``"bottom"``
            or ``"middle"`` or ``"top"`` and horizontal is ``"left"`` or
            ``"center"`` or ``"right"``.

        :param fontsize: (optional)
            The fontsize to use.

        :param rect_params: (optional)
            A dictionary of parameters to pass to the
            :class:`matplotlib.patches.Rectangle` constructor.

        """
        if isinstance(plate, Plate):
            _plate = plate
        else:
            _plate = Plate(
                plate,
                label,
                label_offset,
                shift,
                position,
                fontsize,
                rect_params,
                bbox,
            )

        self._plates.append(_plate)

    def add_text(self, x, y, label, fontsize=None):
        """
        A subclass of plate to writing text using grid coordinates. Any
        ``**kwargs`` are passed through to :class:`PGM.Plate`.

        :param x:
            The x-coordinate of the text in *model units*.

        :param y:
            The y-coordinate of the text.

        :param label:
            A string to write.

        :param fontsize: (optional)
            The fontsize to use.

        """

        text = Text(x=x, y=y, label=label, fontsize=fontsize)
        self._plates.append(text)

        return None

    def render(self, dpi: int | None = None) -> plt.Axes:
        """
        Render the :class:`Plate`, :class:`Edge` and :class:`Node` objects in
        the model. This will create a new figure with the correct dimensions
        and plot the model in this area.

        :param dpi: (optional)
            The DPI value to use for rendering.

        """

        if dpi is None:
            self._ctx.dpi = self._dpi
        else:
            self._ctx.dpi = dpi

        def get_max(maxsize, artist):
            if isinstance(artist, Ellipse):
                maxsize = np.maximum(
                    maxsize,
                    artist.center
                    + np.array([artist.width, artist.height]) / 2,
                    dtype=np.float64,
                )
            elif isinstance(artist, Rectangle):
                maxsize = np.maximum(
                    maxsize,
                    np.array([artist._x0, artist._y0], dtype=np.float64)
                    + np.array([artist._width, artist._height]),
                    dtype=np.float64,
                )
            return maxsize

        def get_min(minsize, artist):
            if isinstance(artist, Ellipse):
                minsize = np.minimum(
                    minsize,
                    artist.center
                    - np.array([artist.width, artist.height]) / 2,
                    dtype=np.float64,
                )
            elif isinstance(artist, Rectangle):
                minsize = np.minimum(
                    minsize,
                    np.array([artist._x0, artist._y0], dtype=np.float64),
                )
            return minsize

        # Auto-set shape
        # We pass through each object once to find the maximum coordinates
        if self.shape is None:
            maxsize = np.copy(self._ctx.origin)

            for plate in self._plates:
                artist = plate.render(self._ctx)
                maxsize = get_max(maxsize, artist)

            for name in self._nodes:
                if self._nodes[name].fixed:
                    self._nodes[name].offset[1] -= 12.5
                artist = self._nodes[name].render(self._ctx)
                maxsize = get_max(maxsize, artist)

            self._ctx.reset_shape(maxsize)

        # Pass through each object to find the minimum coordinates
        if self.origin is None:
            minsize = np.copy(self._ctx.shape * self._ctx.grid_unit)

            for plate in self._plates:
                artist = plate.render(self._ctx)
                minsize = get_min(minsize, artist)

            for name in self._nodes:
                artist = self._nodes[name].render(self._ctx)
                minsize = get_min(minsize, artist)

            self._ctx.reset_origin(minsize, self.shape is None)

        # Clear the figure from rendering context
        self._ctx.reset_figure()

        for plate in self._plates:
            plate.render(self._ctx)

        for edge in self._edges:
            edge.render(self._ctx)

        for name in self._nodes:
            self._nodes[name].render(self._ctx)

        return self.ax

    @property
    def figure(self):
        """Figure as a property."""
        return self._ctx.figure()

    @property
    def ax(self):
        """Axes as a property."""
        return self._ctx.ax()

    def show(self, *args, dpi=None, **kwargs):
        """
        Wrapper on :class:`PGM.render()` that calls `matplotlib.show()`
        immediately after.

        :param dpi: (optional)
            The DPI value to use for rendering.

        """

        self.render(dpi=dpi)
        plt.show(*args, **kwargs)

    def savefig(self, fname, *args, **kwargs):
        """
        Wrapper on ``matplotlib.Figure.savefig()`` that sets default image
        padding using ``bbox_inchaes = tight``.
        ``*args`` and ``**kwargs`` are passed to `matplotlib.Figure.savefig()`.

        :param fname:
            The filename to save as.

        :param dpi: (optional)
            The DPI value to use for saving.

        """
        kwargs["bbox_inches"] = kwargs.get("bbox_inches", "tight")
        kwargs["dpi"] = kwargs.get("dpi", self._dpi)
        if not self.figure:
            self.render()
        self.figure.savefig(fname, *args, **kwargs)
