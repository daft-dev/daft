__all__ = ["PGM", "Node", "Edge", "Plate"]


__version__ = "0.0.1"


import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import FancyArrow
from matplotlib.patches import Rectangle as Rectangle

import numpy as np


class PGM(object):
    """
    The base object for building a graphical model representation.

    :param shape:
        The number of rows and columns in the grid.

    :param origin:
        The coordinates of the bottom left corner of the plot.

    :param grid_size: (optional)
        The size of the grid spacing measured in centimeters.

    :param node_unit: (optional)
        The base unit for the node size. This is a number in centimeters that
        sets the default diameter of the nodes.

    """
    def __init__(self, shape, origin=[0, 0],
            grid_unit=2, node_unit=1,
            observed_style="shaded",
            line_width=1):
        self._nodes = {}
        self._edges = []
        self._plates = []

        self._ctx = _rendering_context(shape=shape, origin=origin,
                grid_unit=grid_unit, node_unit=node_unit,
                observed_style=observed_style, line_width=line_width)

    def add_node(self, node):
        """
        Add a :class:`Node` to the model.

        :param node:
            The :class:`Node` instance to add.

        """
        self._nodes[node.name] = node
        return node

    def add_edge(self, name1, name2, directed=True, **kwargs):
        """
        Construct an :class:`Edge` between two named :class:`Node`s.

        :param name1:
            The name identifying the first node.

        :param name2:
            The name identifying the second node. If the edge is directed,
            the arrow will point to this node.

        :param directed: (optional)
            Should this be a directed edge?

        """
        e = Edge(self._nodes[name1], self._nodes[name2], directed=directed,
                **kwargs)
        self._edges.append(e)
        return e

    def add_plate(self, plate):
        """
        Add a :class:`Plate` object to the model.

        """
        self._plates.append(plate)
        return None

    def render(self):
        """
        Render the :class:`Plate`s, :class:`Edge`s and :class:`Node`s in
        the model. This will create a new figure with the correct dimensions
        and plot the model in this area.

        """
        self.figure = self._ctx.figure()
        self.ax = self._ctx.ax()

        for plate in self._plates:
            plate.render(self._ctx)

        for edge in self._edges:
            edge.render(self._ctx)

        for name, node in self._nodes.iteritems():
            node.render(self._ctx)

        return self.ax


class Node(object):
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

    :param diameter: (optional)
        The diameter (or height) of the node measured in ``node_unit``s as
        defined by the :class:`PGM` object.

    :param aspect: (optional)
        The aspect ratio width/height for elliptical nodes; default 1.

    :param observed: (optional)
        Should this be a conditioned variable?

    :param nogray: (optional)
        Use the double circle rather than gray to indicate conditioning.

    :param fixed: (optional)
        Should this be a fixed (not permitted to vary) variable?
        If `True`, modifies or over-rides diameter, offset, facecolor, etc.
        (Conflicts with `observed`.

    :param plot_params: (optional)
        A dictionary of parameters to pass to the
        :class:`matplotlib.patches.Ellipse` constructor.

    """
    def __init__(self, name, content, x, y, scale=1, aspect=1.,
                 observed=False, fixed=False,
                 offset=[0, 0], plot_params={}):
        # Node style.
        assert not (observed and fixed), \
                "A node cannot be both 'observed' and 'fixed'."
        self.observed = observed
        self.fixed = fixed

        # Metadata.
        self.name = name
        self.content = content

        # Coordinates and dimensions.
        self.x, self.y = x, y
        self.scale = scale
        self.aspect = aspect

        # Display parameters.
        self.plot_params = dict(plot_params)

        # Text parameters.
        self.offset = list(offset)
        self.va = "center"

        # TODO: Make this depend on the node/grid units.
        if self.fixed:
            self.offset[1] += 6
            self.scale /= 6.
            self.va = "bottom"
            self.plot_params["fc"] = "k"

    def render(self, ctx):
        """
        Render the node.

        :param ctx:
            The :class:`_rendering_context` object.

        """
        # Get the axes and default plotting parameters from the rendering
        # context.
        ax = ctx.ax()
        diameter = ctx.node_unit * self.scale

        p = dict(self.plot_params)
        p["lw"] = p.get("lw", ctx.line_width)
        p["ec"] = p.get("ec", "k")
        p["fc"] = p.get("fc", "none")
        p["alpha"] = p.get("alpha", 1)

        # Set up an observed node.
        if self.observed:
            # Update the plotting parameters depending on the style of
            # observed node.
            fc = p["fc"]
            alpha = p["alpha"]
            d = float(diameter)
            if ctx.observed_style == "shaded":
                p["fc"] = "k"
                p["alpha"] = 0.3 * alpha
            elif ctx.observed_style == "outer":
                d = 1.1 * diameter
            elif ctx.observed_style == "innter":
                d = 0.9 * diameter

            # Draw the background ellipse.
            bg = Ellipse(xy=ctx.convert(self.x, self.y),
                         width=d * self.aspect, height=d,
                         **p)
            ax.add_artist(bg)

            # Reset the face color.
            p["fc"] = fc
            p["alpha"] = alpha

        # Draw the foreground ellipse.
        el = Ellipse(xy=ctx.convert(self.x, self.y),
                     width=diameter * self.aspect, height=diameter, **p)
        ax.add_artist(el)

        # Annotate the node.
        ax.annotate(self.content, ctx.convert(self.x, self.y),
                xycoords="data", ha="center", va=self.va,
                xytext=self.offset, textcoords="offset points")

        return el


class Edge(object):
    """
    An edge between two :class:`Node`s.

    :param node1:
        The first :class:`Node`.

    :param node2:
        The second :class:`Node`. The arrow will point towards this node.

    :param directed: (optional)
        Should the edge be directed from ``node1`` to ``node2``? In other
        words: should it have an arrow?

    :param plot_params: (optional)
        A dictionary of parameters to pass to the plotting command when
        rendering.

    """
    def __init__(self, node1, node2, directed=True, plot_params={}):
        self.node1 = node1
        self.node2 = node2
        self.directed = directed
        self.plot_params = plot_params

    def _get_coords(self, ctx):
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

        # Compute the distances.
        dx, dy = x2 - x1, y2 - y1
        dist1 = np.sqrt(dx * dx + dy * dy / float(self.node1.aspect) ** 2)
        dist2 = np.sqrt(dx * dx + dy * dy / float(self.node2.aspect) ** 2)

        # Compute the fractional effect of the radii of the nodes.
        alpha1 = 0.5 * ctx.node_unit * self.node1.scale / dist1
        alpha2 = 0.5 * ctx.node_unit * self.node2.scale / dist2

        # Get the coordinates of the starting position.
        x0, y0 = x1 + alpha1 * dx, y1 + alpha1 * dy

        # Get the width and height of the line.
        dx0 = dx * (1. - alpha1 - alpha2)
        dy0 = dy * (1. - alpha1 - alpha2)

        return x0, y0, dx0, dy0

    def render(self, ctx):
        """
        Render the edge in the given axes.

        :param ax:
            The :class:`matplotlib.Axes` object.

        :param conv:
            A callable coordinate conversion.

        """
        ax = ctx.ax()

        p = self.plot_params

        if self.directed:
            p["ec"] = p.get("ec", "k")
            p["fc"] = p.get("fc", "k")
            p["head_length"] = p.get("head_length", 0.25)
            p["head_width"] = p.get("head_width", 0.1)

            # TODO: make this match the "line_width" property of the context.
            p["width"] = p.get("width", 0.1)
            # p["width"] = p.get("width", (ctx.line_width - 1) / ctx.grid_unit)

            # Build an arrow.
            ar = FancyArrow(*self._get_coords(ctx),
                        length_includes_head=True,
                        **self.plot_params)

            # Add the arrow to the axes.
            ax.add_artist(ar)
            return ar
        else:
            p["color"] = p.get("color", "k")
            p["lw"] = p.get("lw", ctx.line_width - 1)

            # Get the right coordinates.
            x, y, dx, dy = self._get_coords(ctx)

            # Plot the line.
            line = ax.plot([x, x + dx], [y, y + dy], **p)
            return line


class Plate(object):
    """
    A plate to encapsulate repeated independent processes in the model.

    :param rect:
        The rectangle describing the plate bounds in model coordinates.

    :param label: (optional)
        A string to annotate the plate.

    :param label_offset: (optional)
        The x and y offsets of the label text measured in points.

    :param shift: (optional)
        The vertical "shift" of the plate measured in model units. This will
        move the bottom of the panel by ``shift`` units.

    :param rect_params: (optional)
        A dictionary of parameters to pass to the
        :class:`matplotlib.patches.Rectangle` constructor.

    """
    def __init__(self, rect, label=None, label_offset=[5, 5], shift=0,
            rect_params={}):
        self.rect = rect
        self.label = label
        self.label_offset = label_offset
        self.shift = shift
        self.rect_params = rect_params

    def render(self, ctx):
        """
        Render the plate in the given axes.

        :param ax:
            The :class:`matplotlib.Axes` object.

        :param conv:
            A callable coordinate conversion.

        """
        ax = ctx.ax()

        s = np.array([0, self.shift])
        r = np.atleast_1d(self.rect)
        bl = ctx.convert(*(r[:2] + s))
        tr = ctx.convert(*(r[:2] + r[2:]))
        r = np.concatenate([bl, tr - bl])

        p = self.rect_params
        p["ec"] = p.get("ec", "k")
        p["fc"] = p.get("fc", "none")
        p["lw"] = p.get("lw", ctx.line_width)

        rect = Rectangle(r[:2], *r[2:], **self.rect_params)
        ax.add_artist(rect)

        if self.label is not None:
            ax.annotate(self.label, r[:2], xycoords="data",
                    xytext=self.label_offset, textcoords="offset points")

        return rect


class _rendering_context(object):
    """
    :param shape:
        The number of rows and columns in the grid.

    :param origin:
        The coordinates of the bottom left corner of the plot.

    :param grid_unit:
        The size of the grid spacing measured in centimeters.

    :param node_unit:
        The base unit for the node size. This is a number in centimeters that
        sets the default diameter of the nodes.

    """
    def __init__(self, **kwargs):
        # Save the style defaults.
        self.line_width = kwargs.get("line_width", 1.0)

        # Make sure that the observed node style is one that we recognize.
        self.observed_style = kwargs.get("observed_style", "shaded").lower()
        styles = ["shaded", "inner", "outer"]
        assert self.observed_style in styles, \
                "Unrecognized observed node style: {0}\n".format(
                        self.observed_style) \
                + "\tOptions are: {0}".format(", ".join(styles))

        # Set up the figure and grid dimensions.
        self.shape = np.array(kwargs.get("shape", [1, 1]))
        self.origin = np.array(kwargs.get("origin", [0, 0]))
        self.grid_unit = kwargs.get("grid_unit", 2.0)
        self.figsize = self.grid_unit * self.shape / 2.54

        self.node_unit = kwargs.get("node_unit", 1.0)

        # Initialize the figure to ``None`` to handle caching later.
        self._figure = None
        self._ax = None

    def figure(self):
        if self._figure is not None:
            return self._figure
        self._figure = plt.figure(figsize=self.figsize)
        return self._figure

    def ax(self):
        if self._ax is not None:
            return self._ax

        # Add a new axis object if it doesn't exist.
        self._ax = self.figure().add_axes((0, 0, 1, 1), frameon=False,
                xticks=[], yticks=[])

        # Set the bounds.
        l0 = self.convert(*self.origin)
        l1 = self.convert(*(self.origin + self.shape))
        self._ax.set_xlim(l0[0], l1[0])
        self._ax.set_ylim(l0[1], l1[1])

        return self._ax

    def convert(self, *xy):
        """
        Convert from model coordinates to plot coordinates.

        """
        assert len(xy) == 2
        return self.grid_unit * (np.atleast_1d(xy) - self.origin)
