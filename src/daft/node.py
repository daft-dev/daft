"""Node"""

__all__ = ["Node"]

import matplotlib as mpl
from copy import deepcopy
from matplotlib.patches import Ellipse, Rectangle

import numpy as np

from typing import Any, Literal, TypedDict, cast

from .utils import _pop_multiple, RenderingContext
from .types import Tuple2F, CTX_Kwargs, PlotParams, LabelParams, Shape


class Node:
    """
    The representation of a random variable in a :class:`PGM`.

    :param name:
        The plain-text identifier for the node.

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
        If rectangle, aspect and scale holds for rectangle.

    """

    def __init__(
        self,
        name: str,
        content: str,
        x: float,
        y: float,
        scale: float = 1.0,
        aspect: float | None = None,
        observed: bool = False,
        fixed: bool = False,
        alternate: bool = False,
        offset: Tuple2F = (0.0, 0.0),
        fontsize: float | None = None,
        plot_params: PlotParams | None = None,
        label_params: LabelParams | None = None,
        shape: Shape = "ellipse",
    ) -> None:
        # Check Node style.
        # Iterable is consumed, so first condition checks if two or more are
        # true
        node_style = iter((observed, alternate, fixed))
        if not (
            (any(node_style) and not any(node_style))
            or not any((observed, alternate, fixed))
        ):
            msg = "A node cannot be more than one of `observed`, `fixed`, or `alternate`."
            raise ValueError(msg)

        self.observed = observed
        self.fixed = fixed
        self.alternate = alternate

        # Metadata.
        self.name = name
        self.content = content

        # Coordinates and dimensions.
        self.x = float(x)
        self.y = float(y)
        self.scale = float(scale)
        if self.fixed:
            self.scale /= 6.0
        if aspect is not None:
            self.aspect: float | None = float(aspect)
        else:
            self.aspect = aspect

        # Set fontsize
        self.fontsize = fontsize if fontsize else mpl.rcParams["font.size"]

        # Display parameters.
        self.plot_params = cast(PlotParams, dict(plot_params) if plot_params else {})

        # Text parameters.
        self.offset = offset
        self.label_params = cast(LabelParams | None, dict(label_params) if label_params else None)

        # Shape
        if shape in ["ellipse", "rectangle"]:
            self.shape = shape
        else:
            print("Warning: wrong shape value, set to ellipse instead")
            self.shape = "ellipse"

    def render(self, ctx: RenderingContext) -> Ellipse | Rectangle:
        """
        Render the node.

        :param ctx:
            The :class:`_rendering_context` object.

        """
        # Get the axes and default plotting parameters from the rendering
        # context.
        ax = ctx.ax()

        # Resolve the plotting parameters.
        plot_params = cast(PlotParams, dict(self.plot_params))

        plot_params["lw"] = _pop_multiple(
            cast(dict[str, Any], plot_params), ctx.line_width, "lw", "linewidth"
        )

        plot_params["ec"] = plot_params["edgecolor"] = _pop_multiple(
            cast(dict[str, Any], plot_params), ctx.node_ec, "ec", "edgecolor"
        )

        fc_is_set = "fc" in plot_params or "facecolor" in plot_params  # type: ignore[unreachable]
        plot_params["fc"] = _pop_multiple(
            cast(dict[str, Any], plot_params), ctx.node_fc, "fc", "facecolor"
        )
        fc = plot_params["fc"]

        plot_params["alpha"] = plot_params.get("alpha", 1)

        # And the label parameters.
        if self.label_params is None:
            label_params = deepcopy(ctx.label_params)
        else:
            label_params = deepcopy(self.label_params)

        label_params["va"] = _pop_multiple(
            label_params, "center", "va", "verticalalignment"
        )

        label_params["ha"] = _pop_multiple(
            label_params, "center", "ha", "horizontalalignment"
        )

        # Deal with ``fixed`` nodes.
        scale = self.scale
        if self.fixed:
            # MAGIC: These magic numbers should depend on the grid/node units.
            self.offset = (self.offset[0], self.offset[1] + 6)

            label_params["va"] = "baseline"

            if not fc_is_set:
                plot_params["fc"] = "k"


        diameter = ctx.node_unit * scale
        if self.aspect is not None:
            aspect = self.aspect
        else:
            aspect = ctx.aspect

        # Set up an observed node or alternate node. Note the fc INSANITY.
        if self.observed and not self.fixed:
            style = ctx.observed_style
        elif self.alternate and not self.fixed:
            style = ctx.alternate_style
        else:
            style = "none"

        if style != "none":
            # Update the plotting parameters depending on the style of
            # observed node.
            h = float(diameter)
            w = aspect * float(diameter)
            if style == "shaded":
                plot_params["fc"] = "0.7"
            elif style == "outer":
                h = diameter + 0.1 * diameter
                w = aspect * diameter + 0.1 * diameter
            elif style == "inner":
                h = diameter - 0.1 * diameter
                w = aspect * diameter - 0.1 * diameter
                plot_params["fc"] = fc

            # Draw the background ellipse.
            if self.shape == "ellipse":
                bg: Ellipse | Rectangle = Ellipse(
                    xy=ctx.convert(self.x, self.y),
                    width=w,
                    height=h,
                    **plot_params,
                )
            elif self.shape == "rectangle":
                # Adapt to make Rectangle the same api than ellipse
                wi = w
                x, y = ctx.convert(self.x, self.y)
                x -= wi / 2.0
                y -= h / 2.0

                bg = Rectangle(
                    xy=(x, y),
                    width=wi,
                    height=h,
                    **plot_params,
                )
            else:
                # Should never append
                raise (
                    ValueError(
                        "Wrong shape in object causes an error in render"
                    )
                )

            ax.add_artist(bg)

            # Reset the face color.
            plot_params["fc"] = fc

        # Draw the foreground ellipse.
        if not fc_is_set and not self.fixed and self.observed:
            plot_params["fc"] = "none"

        if self.shape == "ellipse":
            el: Ellipse | Rectangle = Ellipse(
                xy=ctx.convert(self.x, self.y),
                width=diameter * aspect,
                height=diameter,
                **plot_params,
            )
        elif self.shape == "rectangle":
            # Adapt to make Rectangle the same api than ellipse
            wi = diameter * aspect
            x, y = ctx.convert(self.x, self.y)
            x -= wi / 2.0
            y -= diameter / 2.0

            el = Rectangle(
                xy=(x, y),
                width=wi,
                height=diameter,
                **plot_params,
            )
        else:
            # Should never append
            raise (
                ValueError("Wrong shape in object causes an error in render")
            )

        ax.add_artist(el)

        # Reset the face color.
        plot_params["fc"] = fc

        # pop extra params
        _label_params = cast(dict[str, Any], label_params)
        _label_params.pop("verticalalignment", None)
        _label_params.pop("ma", None)

        # Annotate the node.
        ax.annotate(
            self.content,
            ctx.convert(self.x, self.y),
            xycoords="data",
            xytext=self.offset,
            textcoords="offset points",
            size=self.fontsize,
            **_label_params,
        )

        return el

    def get_frontier_coord(self, target_xy: Tuple2F, ctx: RenderingContext, edge: 'Edge') -> Tuple2F:
        """
        Get the coordinates of the point of intersection between the
        shape of the node and a line starting from the center of the node to an
        arbitrary point. Will throw a :class:`SameLocationError` if the nodes
        contain the same `x` and `y` coordinates. See the example of rectangle
        below:

        .. code-block:: python

            _____________
            |            |    ____--X (target_node)
            |        __--X----
            |     X--    |(return coordinate of this point)
            |            |
            |____________|

        :target_xy: (x float, y float)
            A tuple of coordinate of target node

        """

        # Scale the coordinates appropriately.
        x1, y1 = ctx.convert(self.x, self.y)
        x2, y2 = target_xy[0], target_xy[1]

        # Aspect ratios.
        if self.aspect is not None:
            aspect = self.aspect
        else:
            aspect = ctx.aspect

        if self.shape == "ellipse":
            # Compute the distances.
            dx, dy = x2 - x1, y2 - y1
            if dx == 0.0 and dy == 0.0:
                raise SameLocationError(edge)
            dist1 = np.sqrt(dy * dy + dx * dx / float(aspect * aspect))

            # Compute the fractional effect of the radii of the nodes.
            alpha1 = 0.5 * ctx.node_unit * self.scale / dist1

            # Get the coordinates of the starting position.
            x0, y0 = x1 + alpha1 * dx, y1 + alpha1 * dy

            return x0, y0

        elif self.shape == "rectangle":
            dx, dy = x2 - x1, y2 - y1

            # theta = np.angle(complex(dx, dy))
            # print(theta)
            # left or right intersection
            dxx1 = self.scale * aspect / 2.0 * (np.sign(dx) or 1.0)
            dyy1 = (
                self.scale
                * aspect
                / 2.0
                * np.abs(dy / dx)
                * (np.sign(dy) or 1.0)
            )
            val1 = np.abs(complex(dxx1, dyy1))

            # up or bottom intersection
            dxx2 = self.scale * 0.5 * np.abs(dx / dy) * (np.sign(dx) or 1.0)
            dyy2 = self.scale * 0.5 * (np.sign(dy) or 1.0)
            val2 = np.abs(complex(dxx2, dyy2))

            if val1 < val2:
                return x1 + dxx1, y1 + dyy1
            else:
                return x1 + dxx2, y1 + dyy2

        else:
            # Should never append
            raise ValueError("Wrong shape in object causes an error")


from .edge import Edge
from .exceptions import SameLocationError
