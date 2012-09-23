__all__ = ["PGM", "Node", "Edge", "Plate"]


__version__ = "0.0.1"


import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import FancyArrow as Arrow
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

    """
    def __init__(self, shape, origin=[0, 0], grid_size=2):
        self.shape = np.array(shape)
        self.origin = np.array(origin)
        self.grid_size = grid_size
        self._figsize = grid_size * self.shape / 2.54

        self._nodes = {}
        self._edges = []
        self._plates = []

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
        self.figure = plt.figure(figsize=self._figsize)
        self.ax = self.figure.add_axes((0, 0, 1, 1), frameon=False,
                xticks=[], yticks=[])

        # Set the bounds of the plot.
        l0 = self._convert_coords(*self.origin)
        l1 = self._convert_coords(*(self.origin + self.shape))
        self.ax.set_xlim(l0[0], l1[0])
        self.ax.set_ylim(l0[1], l1[1])

        for plate in self._plates:
            plate.render(self.ax, self._convert_coords)

        for edge in self._edges:
            edge.render(self.ax, self._convert_coords)

        for name, node in self._nodes.iteritems():
            node.render(self.ax, self._convert_coords)

        return self.ax

    def _convert_coords(self, *xy):
        """
        Convert from model coordinates to plot coordinates.

        """
        assert len(xy) == 2
        return self.grid_size * (np.atleast_1d(xy) - self.origin)


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
        The diameter (or height) of the node measured in centimeters.

    :param aspect: (optional)
        The aspect ratio width/height for elliptical nodes; default 1.

    :param observed: (optional)
        Should this be a conditioned variable?

    :param plot_params: (optional)
        A dictionary of parameters to pass to the
        :class:`matplotlib.patches.Ellipse` constructor.

    """
    def __init__(self, name, content, x, y, diameter=3, aspect=1.,
                 observed=False, offset=[0, 0], plot_params={}):
        self.name = name
        self.content = content
        self.x = x
        self.y = y
        self.diameter = diameter / 2.54
        self.aspect = aspect
        self.observed = observed
        self.offset = offset
        self.plot_params = plot_params

    def render(self, ax, conv):
        """
        Render the node.

        :param ax:
            The :class:`matplotlib.Axes` object to plot into.

        :param conv:
            A callable coordinate conversion.

        """
        p = dict(self.plot_params)
        p["ec"] = p.get("ec", "k")
        p["fc"] = p.get("fc", "none")

        # Set up an observed node.
        if self.observed:
            p["fc"] = "k"
            p["alpha"] = 0.3

            # Draw the background ellipse.
            bg = Ellipse(xy=conv(self.x, self.y),
                         width=self.diameter * self.aspect,
                         height=self.diameter, **p)
            ax.add_artist(bg)

            # Reset the face color.
            p["fc"] = "none"
            p["alpha"] = 1

        # Draw the foreground ellipse.
        el = Ellipse(xy=conv(self.x, self.y),
                     width=self.diameter * self.aspect,
                     height=self.diameter, **p)
        ax.add_artist(el)

        # Annotate the node.
        ax.annotate(self.content, conv(self.x, self.y),
                xycoords="data", ha="center", va="center",
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

    def _get_coords(self, conv):
        """
        Get the coordinates of the line.

        :param conv:
            A callable coordinate conversion.

        :returns:
            * ``x0``, ``y0``: the coordinates of the start of the line.
            * ``dx0``, ``dy0``: the displacement vector.

        """
        # Scale the coordinates appropriately.
        x1, y1 = conv(self.node1.x, self.node1.y)
        x2, y2 = conv(self.node2.x, self.node2.y)

        # Compute the distances.
        dx, dy = x2 - x1, y2 - y1
        dist1 = np.sqrt(dx * dx + dy * dy / float(self.node1.aspect) ** 2)
        dist2 = np.sqrt(dx * dx + dy * dy / float(self.node2.aspect) ** 2)

        # Compute the fractional effect of the radii of the nodes.
        alpha1 = 0.5 * self.node1.diameter / dist1
        alpha2 = 0.5 * self.node2.diameter / dist2

        # Get the coordinates of the starting position.
        x0, y0 = x1 + alpha1 * dx, y1 + alpha1 * dy

        # Get the width and height of the line.
        dx0 = dx * (1. - alpha1 - alpha2)
        dy0 = dy * (1. - alpha1 - alpha2)

        return x0, y0, dx0, dy0

    def render(self, ax, conv):
        """
        Render the edge in the given axes.

        :param ax:
            The :class:`matplotlib.Axes` object.

        :param conv:
            A callable coordinate conversion.

        """
        p = self.plot_params
        if self.directed:
            p["ec"] = p.get("ec", "k")
            p["fc"] = p.get("fc", "k")
            p["head_length"] = p.get("head_length", 0.25)
            p["head_width"] = p.get("head_width", 0.1)

            # Build an arrow.
            ar = Arrow(*self._get_coords(conv),
                        length_includes_head=True, width=0.,
                        **self.plot_params)

            # Add the arrow to the axes.
            ax.add_artist(ar)
            return ar
        else:
            p["color"] = p.get("color", "k")

            # Get the right coordinates.
            x, y, dx, dy = self._get_coords(conv)

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

    def render(self, ax, conv):
        """
        Render the plate in the given axes.

        :param ax:
            The :class:`matplotlib.Axes` object.

        :param conv:
            A callable coordinate conversion.

        """
        s = np.array([0, self.shift])
        r = np.atleast_1d(self.rect)
        bl = conv(*(r[:2] + s))
        tr = conv(*(r[:2] + r[2:]))
        r = np.concatenate([bl, tr - bl])

        p = self.rect_params
        p["ec"] = p.get("ec", "k")
        p["fc"] = p.get("fc", "none")

        rect = Rectangle(r[:2], *r[2:], **self.rect_params)

        ax.add_artist(rect)

        if self.label is not None:
            ax.annotate(self.label, r[:2], xycoords="data",
                    xytext=self.label_offset, textcoords="offset points")

        return rect
