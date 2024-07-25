"""Edge"""

__all__ = ["Edge"]


from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrow

from typing import Any, cast

from ._utils import _pop_multiple, _RenderingContext
from ._types import Tuple4F, PlotParams, LabelParams


class Edge:
    """
    An edge between two :class:`Node` objects.

    :param node1:
        The first :class:`Node`.

    :param node2:
        The second :class:`Node`. The arrow will point towards this node.

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
        :class:`matplotlib.patches.FancyArrow` constructor to adjust
        edge behavior.

    :param label_params: (optional)
        A dictionary of parameters to pass to the
        :class:`matplotlib.axes.Axes.annotate` constructor to adjust
        label behavior.

    """

    def __init__(
        self,
        node1: 'Node',
        node2: 'Node',
        directed: bool = True,
        label: str | None = None,
        xoffset: float = 0,
        yoffset: float = 0.1,
        plot_params: PlotParams | None = None,
        label_params: LabelParams | None = None,
    ) -> None:
        self.node1 = node1
        self.node2 = node2
        self.directed = directed
        self.label = label
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.plot_params = dict(plot_params) if plot_params else {}
        self.label_params = dict(label_params) if label_params else {}

    def _get_coords(self, ctx: _RenderingContext) -> Tuple4F:
        """
        Get the coordinates of the line.

        :param conv:
            A callable coordinate conversion.

        :returns:
            * ``x0``, ``y0``: the coordinates of the start of the line.
            * ``dx0``, ``dy0``: the displacement vector.

        """
        # Scale the coordinates appropriately.
        x1, y1 = ctx.convert(self.node1.x, self.node1.y)
        x2, y2 = ctx.convert(self.node2.x, self.node2.y)

        x3, y3 = self.node1.get_frontier_coord((x2, y2), ctx, self)
        x4, y4 = self.node2.get_frontier_coord((x1, y1), ctx, self)

        return x3, y3, x4 - x3, y4 - y3

    def render(self, ctx: _RenderingContext) -> FancyArrow | list[Line2D]:
        """
        Render the edge in the given axes.

        :param ctx:
            The :class:`_rendering_context` object.

        """
        ax = ctx.ax()

        plot_params = self.plot_params
        plot_params["linewidth"] = _pop_multiple(
            plot_params, ctx.line_width, "lw", "linewidth"
        )

        plot_params["linestyle"] = plot_params.get("linestyle", "-")

        # Add edge annotation.
        if self.label is not None:
            x, y, dx, dy = self._get_coords(ctx)
            ax.annotate(
                self.label,
                xy=(x + 0.5 * dx + self.xoffset, y + 0.5 * dy + self.yoffset),
                xycoords="data",
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="center",
                **cast(dict[str, Any], self.label_params)
            )

        if self.directed:
            plot_params["ec"] = _pop_multiple(
                plot_params, "k", "ec", "edgecolor"
            )
            plot_params["fc"] = _pop_multiple(
                plot_params, "k", "fc", "facecolor"
            )
            plot_params["head_length"] = plot_params.get("head_length", 0.25)
            plot_params["head_width"] = plot_params.get("head_width", 0.1)

            # Build an arrow.
            args = self._get_coords(ctx)

            # zero lengh arrow produce error
            if not (args[2] == 0.0 and args[3] == 0.0):
                ar = FancyArrow(
                    *self._get_coords(ctx),
                    width=0,
                    length_includes_head=True,
                    **cast(dict[str, Any], plot_params)
                )

                # Add the arrow to the axes.
                ax.add_artist(ar)
                return ar

            else:
                print(args[2], args[3])
                return []

        else:
            plot_params["color"] = plot_params.get("color", "k")

            # Get the right coordinates.
            x, y, dx, dy = self._get_coords(ctx)

            # Plot the line.
            line = ax.plot(
                (x, x + dx),
                (y, y + dy),
                **cast(dict[str, Any], plot_params)
            )
            return line


from .node import Node
