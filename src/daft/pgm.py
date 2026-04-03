"""Code for Daft"""

__all__ = ["PGM"]
# TODO: should Text be added?

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle

import numpy as np

from typing import Any, Optional, Union

from .node import Node
from .edge import Edge
from .plate import Plate, Text
from .utils import RenderingContext
from .types import (
    Tuple2F,
    NDArrayF,
    Shape,
    Position,
    CTX_Kwargs,
    PlotParams,
    LabelParams,
    RectParams,
)

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
        shape: Optional[Tuple2F] = None,
        origin: Optional[Tuple2F] = None,
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
        label_params: Optional[LabelParams] = None,
        dpi: Optional[int] = None,
    ) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: list[Edge] = []
        self._plates: list[Plate] = []
        self._dpi = dpi

        # if shape and origin are not given, pass a default
        # and we will determine at rendering time
        if shape is None:
            _shape: Tuple2F = (1, 1)
            self.shape = None
        else:
            _shape = shape
            self.shape = tuple(shape)

        if origin is None:
            _origin: Tuple2F = (0, 0)
            self.origin = None
        else:
            _origin = origin
            self.origin = tuple(origin)

        self._ctx = RenderingContext(
            CTX_Kwargs(
                shape=np.asarray(_shape, dtype=np.float64),
                origin=np.asarray(_origin, dtype=np.float64),
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
        )

    def __enter__(self) -> "PGM":
        return self

    def __exit__(self, *args: Any) -> None:
        self._ctx.close()

    def add_node(
        self,
        node: Node,
        content: str = "",
        x: float = 0,
        y: float = 0,
        scale: float = 1.0,
        aspect: Optional[float] = None,
        observed: bool = False,
        fixed: bool = False,
        alternate: bool = False,
        offset: Tuple2F = (0, 0),
        fontsize: Optional[float] = None,
        plot_params: Optional[PlotParams] = None,
        label_params: Optional[LabelParams] = None,
        shape: Shape = "ellipse",
    ) -> Node:
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
            _node = Node(  # type: ignore[unreachable]
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
        name1: str,
        name2: str,
        directed: Optional[bool] = None,
        xoffset: float = 0.0,
        yoffset: float = 0.1,
        label: Optional[str] = None,
        plot_params: Optional[PlotParams] = None,
        label_params: Optional[LabelParams] = None,
        **kwargs: dict[str, Any],  # pylint: disable=unused-argument
    ) -> Edge:
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
        plate: Plate,
        label: Optional[str] = None,
        label_offset: Tuple2F = (5, 5),
        shift: float = 0,
        position: Position = "bottom left",
        fontsize: Optional[float] = None,
        rect_params: Optional[RectParams] = None,
        bbox: Optional[bool] = None,
    ) -> None:
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
            _plate = Plate(  # type: ignore[unreachable]
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

    def add_text(
        self, x: float, y: float, label: str, fontsize: Optional[float] = None
    ) -> None:
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

    def render(self, dpi: Optional[int] = None) -> plt.Axes:
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

        def get_max(
            maxsize: NDArrayF, patch: Union[Ellipse, Rectangle]
        ) -> NDArrayF:
            if isinstance(patch, Ellipse):
                maxsize = np.maximum(
                    maxsize,
                    patch.center + np.array([patch.width, patch.height]) / 2,
                    dtype=np.float64,
                )
            elif isinstance(patch, Rectangle):
                maxsize = np.maximum(
                    maxsize,
                    np.array([patch._x0, patch._y0], dtype=np.float64)  # type: ignore[attr-defined]
                    + np.array([patch._width, patch._height]),  # type: ignore[attr-defined]
                    dtype=np.float64,
                )
            return maxsize

        def get_min(
            minsize: NDArrayF, patch: Union[Ellipse, Rectangle]
        ) -> NDArrayF:
            if isinstance(patch, Ellipse):
                minsize = np.minimum(
                    minsize,
                    patch.center - np.array([patch.width, patch.height]) / 2,
                    dtype=np.float64,
                )
            elif isinstance(patch, Rectangle):
                minsize = np.minimum(
                    minsize,
                    np.array([patch._x0, patch._y0], dtype=np.float64),  # type: ignore[attr-defined]
                )
            return minsize

        # Auto-set shape
        # We pass through each object once to find the maximum coordinates
        if self.shape is None:
            maxsize = np.copy(self._ctx.origin)

            for plate in self._plates:
                artist: Union[Ellipse, Rectangle] = plate.render(self._ctx)
                maxsize = get_max(maxsize, artist)

            for name in self._nodes:
                if self._nodes[name].fixed:
                    offx, offy = self._nodes[name].offset
                    offy -= 12.5
                    self._nodes[name].offset = (offx, offy)

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
    def figure(self) -> plt.Figure:
        """Figure as a property."""
        return self._ctx.figure()

    @property
    def ax(self) -> plt.Axes:
        """Axes as a property."""
        return self._ctx.ax()

    def show(
        self, *args: Any, dpi: Optional[int] = None, **kwargs: Any
    ) -> None:
        """
        Wrapper on :class:`PGM.render()` that calls `matplotlib.show()`
        immediately after.

        :param dpi: (optional)
            The DPI value to use for rendering.

        """

        self.render(dpi=dpi)
        plt.show(*args, **kwargs)

    def savefig(self, fname: str, *args: Any, **kwargs: Any) -> None:
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
        self.figure.savefig(fname, *args, **kwargs)
